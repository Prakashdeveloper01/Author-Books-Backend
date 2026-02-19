
    
from typing import Optional
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException, status
import uuid
from datetime import timedelta
from app.utils.schema_utils import JWTPayloadSchema
from datetime import timezone
from datetime import datetime
from app.config import CONFIG_SETTINGS
import jwt
from redis import asyncio as aioredis

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=CONFIG_SETTINGS.ROOT_PATH + "/utils/token")


class JWTService:
    """JWT authentication service with async Redis, with full claim generation and validation."""

    def __init__(self) -> None:
        self.redis_client = aioredis.Redis(
            host=CONFIG_SETTINGS.REDIS_DB_HOST,
            port=CONFIG_SETTINGS.REDIS_PORT,
            db=CONFIG_SETTINGS.REDIS_DB,
            password=CONFIG_SETTINGS.REDIS_PASS,
            ssl=bool(CONFIG_SETTINGS.SSL_CA_CERTS),
            ssl_ca_certs=CONFIG_SETTINGS.SSL_CA_CERTS or None,
            decode_responses=True,
        )

        # Defaults for issuer/audience if not configured
        self.issuer = CONFIG_SETTINGS.PROJECT_NAME
        self.audience = "api"

    def _now(self) -> datetime:
        """UTC now helper."""
        return datetime.now(timezone.utc)

    def _int_ts(self, dt: datetime) -> int:
        """Return integer timestamp for pyjwt claims (seconds)."""
        return int(dt.timestamp())

    async def create_access_token(self, data: JWTPayloadSchema) -> str:
        """Generate a new access token including standard claims + jti, and store JTI + token in Redis."""
        # compute expiry
        expire_dt = self._now() + timedelta(minutes=CONFIG_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
        iat_dt = self._now()
        nbf_dt = iat_dt  # immediately valid; adjust if you want a delay
        jti_str = uuid.uuid4().hex

        # Build payload dict from schema (do not mutate original schema object)
        payload = data.model_dump()
        # Standard claims (use numeric timestamps)
        payload.update(
            {
                "iss": self.issuer,
                "aud": self.audience,
                "iat": self._int_ts(iat_dt),
                "nbf": self._int_ts(nbf_dt),
                "exp": self._int_ts(expire_dt),
                "jti": jti_str,
            }
        )

        private_key = CONFIG_SETTINGS.APP_JWT_PRIVATE_KEY.replace("\\n", "\n")
        token = jwt.encode(payload, private_key, algorithm="RS256")

        # Redis keys and expirations (seconds)
        access_redis_key = f"access_token:{payload['uuid']}"
        jti_redis_key = f"jti:{jti_str}"
        expire_seconds = max(1, int((expire_dt - self._now()).total_seconds()))

        # Blacklist old token (if any)
        old_token = await self.redis_client.get(access_redis_key)
        if old_token:
            # keep prior behavior: blacklisting previous token so it can't be reused
            await self.redis_client.setex(
                f"blacklisted_token:{old_token}",
                (CONFIG_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES + 10) * 60,
                old_token,
            )

        # store new token and its jti
        await self.redis_client.delete(access_redis_key)
        await self.redis_client.setex(access_redis_key, (CONFIG_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES + 10) * 60, token)
        await self.redis_client.setex(jti_redis_key, expire_seconds, payload["uuid"])

        return token

    async def create_refresh_token(self, data: JWTPayloadSchema) -> str:
        """Generate a new refresh token including standard claims + jti, and store JTI + token in Redis."""
        expire_dt = self._now() + timedelta(minutes=CONFIG_SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES)
        iat_dt = self._now()
        nbf_dt = iat_dt
        jti_str = uuid.uuid4().hex

        payload = data.model_dump()
        payload.update(
            {
                "iss": self.issuer,
                "aud": self.audience,
                "iat": self._int_ts(iat_dt),
                "nbf": self._int_ts(nbf_dt),
                "exp": self._int_ts(expire_dt),
                "jti": jti_str,
            }
        )

        private_key = CONFIG_SETTINGS.APP_JWT_PRIVATE_KEY.replace("\\n", "\n")
        token = jwt.encode(payload, private_key, algorithm="RS256")

        refresh_redis_key = f"refresh_token:{payload['uuid']}"
        refresh_jti_key = f"refresh_jti:{jti_str}"
        expire_seconds = max(1, int((expire_dt - self._now()).total_seconds()))

        await self.redis_client.delete(refresh_redis_key)
        await self.redis_client.setex(refresh_redis_key, (CONFIG_SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES + 20) * 60, token)
        await self.redis_client.setex(refresh_jti_key, expire_seconds, payload["uuid"])

        return token
    async def force_to_expire_token(self, uuid: str) -> None:
        """Force the current access token to expire (blacklist it)."""
        expire_redis_key = f"expire_token:{uuid}"
        await self.redis_client.setex(expire_redis_key, CONFIG_SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES, uuid)

    async def delete_expire_token(self, uuid: str) -> None:
        """Delete the expire token key."""
        expire_redis_key = f"expire_token:{uuid}"
        await self.redis_client.delete(expire_redis_key)






    async def _decode_and_verify(self, token: str, verify_exp: bool = True) -> dict:
        """
        Decode and verify token with public key, issuer and audience.
        verify_exp controls expiraton verification (only used for special flows).
        """
        public_key = CONFIG_SETTINGS.APP_JWT_PUBLIC_KEY.replace("\\n", "\n")
        options = {"verify_exp": verify_exp}
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options=options,
                issuer=self.issuer,
                audience=self.audience,
            )
            return payload
        except jwt.ExpiredSignatureError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token expired") from err
        except jwt.InvalidIssuerError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token) from err
        except jwt.InvalidAudienceError as err:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token) from err
        except jwt.PyJWTError as err:
            # Generic decode error
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token) from err
        

    async def verify_refresh_token(self, token: str) -> JWTPayloadSchema:
        """Verify the refresh token and return the payload if valid."""
        # fully verify claims (including exp, iss, aud)
        payload = await self._decode_and_verify(token, verify_exp=True)

        # verify refresh token matches stored token for user uuid
        redis_key = f"refresh_token:{payload['uuid']}"
        stored_token = await self.redis_client.get(redis_key)
        if not stored_token or stored_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.message.invalid_token)

        # verify jti exists and maps to uuid (replay protection)
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token)

        refresh_jti_key = f"refresh_jti:{jti}"
        stored_uuid_for_jti = await self.redis_client.get(refresh_jti_key)
        if not stored_uuid_for_jti or stored_uuid_for_jti != payload["uuid"]:
            # token was replayed or jti missing
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token)

        return JWTPayloadSchema(**payload)

    async def verify_access_token(self, token: str) -> JWTPayloadSchema:
        """Verify the access token and return the payload if valid."""
        # quick blacklist check (old tokens that were intentionally blacklisted)
        black_list_redis_key = f"blacklisted_token:{token}"
        black_list_token = await self.redis_client.get(black_list_redis_key)
        if black_list_token:
            # delete blacklist entry to prevent reuse of the same blacklist marker
            await self.redis_client.delete(black_list_redis_key)
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=self.message.your_section_used)


        # decode & verify claims (exp, iss, aud, etc.)
        payload = await self._decode_and_verify(token, verify_exp=True)
        expire_redis_key = f"expire_token:{payload['uuid']}"

        # Ensure token is the active token for that user (single-session)
        redis_key = f"access_token:{payload['uuid']}"
        stored_token = await self.redis_client.get(redis_key)
        if not stored_token or stored_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token)

        # Verify JTI exists and maps to the UUID (replay protection)
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token)
        jti_key = f"jti:{jti}"
        stored_uuid_for_jti = await self.redis_client.get(jti_key)
        if not stored_uuid_for_jti or stored_uuid_for_jti != payload["uuid"]:
            # jti not present or doesn't match uuid -> possible replay or revoked token
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=self.message.invalid_token)
        get_expire = await self.redis_client.get(expire_redis_key)
        if get_expire:
            await self.delete_expire_token(payload['uuid'])
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")

        return JWTPayloadSchema(**payload)

    async def revoke_token(self, uuid: str) -> None:
        """Revoke both access and refresh tokens for a user, and remove associated JTIs."""
        # delete stored token values
        access_token = await self.redis_client.get(f"access_token:{uuid}")
        refresh_token = await self.redis_client.get(f"refresh_token:{uuid}")

        # If tokens found, attempt to decode them (without verifying exp) to remove their jtis
        public_key = CONFIG_SETTINGS.APP_JWT_PUBLIC_KEY.replace("\\n", "\n")
        for token in (access_token, refresh_token):
            if token:
                try:
                    payload = jwt.decode(token, public_key, algorithms=["RS256"], options={"verify_exp": False})
                    jti = payload.get("jti")
                    if jti:
                        await self.redis_client.delete(f"jti:{jti}")
                        await self.redis_client.delete(f"refresh_jti:{jti}")
                except jwt.PyJWTError:
                    # ignore decode errors on cleanup
                    pass

        await self.redis_client.delete(f"access_token:{uuid}")
        await self.redis_client.delete(f"refresh_token:{uuid}")

    async def uuid_to_token(self, uuid: str) -> Optional[str]:
        """Get the access token associated with a UUID, returning None if invalid/expired."""
        redis_key = f"access_token:{uuid}"
        token = await self.redis_client.get(redis_key)

        if not token:
            return None

        # decode without verifying exp to read payload safely
        public_key = CONFIG_SETTINGS.APP_JWT_PUBLIC_KEY.replace("\\n", "\n")
        options = {"verify_exp": True}
        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                options=options,
                issuer=self.issuer,
                audience=self.audience,
            )
        except jwt.DecodeError:
            return None
        except Exception as exc:
            return None

        # Check expiry claim manually (payload['exp'] is int seconds)
        exp = payload.get("exp")
        if exp is not None and exp < int(self._now().timestamp()):
            return None

        return token


# ----------------------------
# FastAPI dependencies
# ----------------------------
async def get_current_user( token: str = Depends(oauth2_scheme)):
    check = await JWTService().verify_access_token(token)
    return JWTPayloadSchema(**check.model_dump())