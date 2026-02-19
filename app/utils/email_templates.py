def create_otp_email_template(otp_code: str) -> str:
    """
    Generates a professional, premium HTML email template for sending OTP codes.
    Follows modern design principles with a clean layout, proper typography, and responsive structure.
    """
    return f"""
<!DOCTYPE html>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
    <meta charset="utf-8"> <!-- utf-8 works for most cases -->
    <meta name="viewport" content="width=device-width"> <!-- Forcing initial-scale shouldn't be necessary -->
    <meta http-equiv="X-UA-Compatible" content="IE=edge"> <!-- Use the latest (edge) version of IE rendering engine -->
    <meta name="x-apple-disable-message-reformatting">  <!-- Disable auto-scale in iOS 10 Mail entirely -->
    <title>Verification Code</title> <!-- The title tag shows in email notifications, like Android 4.4. -->

    <link href="https://fonts.googleapis.com/css?family=Inter:400,600,700&display=swap" rel="stylesheet">

    <!-- Web Font / @font-face : BEGIN -->
    <!-- NOTE: If web fonts are not required, lines 10 - 27 can be safely removed. -->

    <!-- CSS Reset : BEGIN -->
    <style>
        /* What it does: Remove spaces around the email design added by some email clients. */
        /* Beware: It can remove the padding / margin and add a background color to the compose a reply window. */
        html,
        body {{
            margin: 0 auto !important;
            padding: 0 !important;
            height: 100% !important;
            width: 100% !important;
            background-color: #f4f7f6;
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}

        /* What it does: Stops email clients resizing small text. */
        * {{
            -ms-text-size-adjust: 100%;
            -webkit-text-size-adjust: 100%;
        }}

        /* What it does: Centers email on Android 4.4 */
        div[style*="margin: 16px 0"] {{
            margin: 0 !important;
        }}

        /* What it does: Stops Outlook from adding extra spacing to tables. */
        table,
        td {{
            mso-table-lspace: 0pt !important;
            mso-table-rspace: 0pt !important;
        }}

        /* What it does: Fixes webkit padding issue. */
        table {{
            border-spacing: 0 !important;
            border-collapse: collapse !important;
            table-layout: fixed !important;
            margin: 0 auto !important;
        }}

        /* What it does: Uses a better rendering method when resizing images in IE. */
        img {{
            -ms-interpolation-mode:bicubic;
        }}

        /* What it does: Prevents Windows 10 Mail from underlining links despite inline CSS. Styles for underlined links should be inline. */
        a {{
            text-decoration: none;
        }}

        /* What it does: A work-around for email clients meddling in triggered links. */
        *[x-apple-data-detectors],  /* iOS */
        .unstyle-auto-detected-links *,
        .aBn {{
            border-bottom: 0 !important;
            cursor: default !important;
            color: inherit !important;
            text-decoration: none !important;
            font-size: inherit !important;
            font-family: inherit !important;
            font-weight: inherit !important;
            line-height: inherit !important;
        }}

        /* What it does: Prevents Gmail from displaying a download button on large, non-linked images. */
        .a6S {{
            display: none !important;
            opacity: 0.01 !important;
        }}

        /* What it does: Prevents Gmail from changing the text color in conversation view. */
        .im {{
            color: inherit !important;
        }}

        /* What it does: Removes right gutter in Gmail iOS app: https://github.com/tedgoas/Cerberus/issues/89  */
        /* Create one of these media queries for each additional viewport size you'd like to fix */

        /* iPhone 4, 4S, 5, 5S, 5C, and 5SE */
        @media only screen and (min-device-width: 320px) and (max-device-width: 374px) {{
            .email-container {{
                min-width: 320px !important;
            }}
        }}
        /* iPhone 6, 6S, 7, 8, and X */
        @media only screen and (min-device-width: 375px) and (max-device-width: 413px) {{
            .email-container {{
                min-width: 375px !important;
            }}
        }}
        /* iPhone 6+, 7+, and 8+ */
        @media only screen and (min-device-width: 414px) {{
            .email-container {{
                min-width: 414px !important;
            }}
        }}

    </style>
    <!-- CSS Reset : END -->

    <!-- Progressive Enhancements : BEGIN -->
    <style>

	    .button-td,
	    .button-a {{
	        transition: all 100ms ease-in;
	    }}
	    .button-td-primary:hover,
	    .button-a-primary:hover {{
	        background: #555555 !important;
	        border-color: #555555 !important;
	    }}

    </style>
    <!-- Progressive Enhancements : END -->

</head>
<body width="100%" style="margin: 0; padding: 0 !important; mso-line-height-rule: exactly; background-color: #f4f7f6;">
	<center style="width: 100%; background-color: #f4f7f6;">
    <!--[if mso | IE]>
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f4f7f6;">
    <tr>
    <td>
    <![endif]-->

        <!-- Visually Hidden Preheader Text : BEGIN -->
        <div style="display: none; font-size: 1px; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; mso-hide: all; font-family: sans-serif;">
            Your secure verification code is here. Valid for 5 minutes.
        </div>
        <!-- Visually Hidden Preheader Text : END -->

        <!-- Create white space after the visual preheader and before the email content -->
        <!--[if mso | IE]>
        <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="600" align="center" style="width:600px;">
        <tr>
        <td style="line-height:0px;font-size:0px;mso-line-height-rule:exactly;">
        <![endif]-->
        <div style="max-width: 600px; margin: 0 auto;" class="email-container">
            <!--[if mso | IE]>
            </td>
            </tr>
            </table>
            <![endif]-->
        </div>
        <!--[if mso | IE]>
        </td>
        </tr>
        </table>
        <![endif]-->

        <!-- Email Body : BEGIN -->
        <table align="center" role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="margin: auto;">
	        <!-- Email Header : BEGIN -->
            <tr>
                <td style="padding: 40px 0; text-align: center">
                   <h1 style="margin: 0; font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 700; color: #2d3748; letter-spacing: -0.5px;">Author Books</h1>
                </td>
            </tr>
	        <!-- Email Header : END -->

            <!-- Main Content : BEGIN -->
            <tr>
                <td valign="middle" class="hero bg_white" style="padding: 0;">
                    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%">
                        <tr>
                            <td style="padding: 0;">
                                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
                                    <tr>
                                        <td style="padding: 40px 50px;">
                                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                                <tr>
                                                    <td style="text-align: left; padding-bottom: 20px;">
                                                        <h2 style="margin: 0; color: #1a202c; font-family: 'Inter', sans-serif; font-size: 24px; font-weight: 700; line-height: 1.4;">Verify your identity</h2>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="text-align: left; padding-bottom: 30px;">
                                                        <p style="margin: 0; color: #4a5568; font-family: 'Inter', sans-serif; font-size: 16px; line-height: 1.6;">
                                                            Hello,
                                                            <br><br>
                                                            We received a request to access your Author Books account. Use the code below to complete the verification process.
                                                        </p>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td align="center" style="padding-bottom: 30px;">
                                                        <div style="background-color: #f7fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; display: inline-block; min-width: 200px;">
                                                            <span style="font-family: 'Inter', monospace; font-size: 32px; font-weight: 700; color: #2d3748; letter-spacing: 6px; display: block; text-align: center;">{otp_code}</span>
                                                        </div>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="text-align: left;">
                                                        <p style="margin: 0; color: #718096; font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.6;">
                                                            This code is valid for <strong>5 minutes</strong>. If you didn't request this code, you can safely ignore this email.
                                                        </p>
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
            <!-- Main Content : END -->

            <!-- Footer : BEGIN -->
            <tr>
                <td style="padding: 30px 0; text-align: center;">
                    <div style="max-width: 600px; margin: 0 auto;">
                        <p style="margin: 0; font-family: 'Inter', sans-serif; font-size: 12px; line-height: 1.5; color: #a0aec0;">
                            &copy; 2026 Author Books. All rights reserved.<br>
                            This is an automated system email. Please do not reply.
                        </p>
                    </div>
                </td>
            </tr>
            <!-- Footer : END -->

        </table>
        <!-- Email Body : END -->

    <!--[if mso | IE]>
    </td>
    </tr>
    </table>
    <![endif]-->
    </center>
</body>
</html>
"""
