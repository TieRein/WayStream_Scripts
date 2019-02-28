/* Author: Jacob Chesley
*
*  Node.js script to send confirmation emails
*
*  Last Updated: 2/4/19
*/

const nodemailer = require('nodemailer');
const adminEmail = require('./config').EMAIL_CONFIG;
const serverHostname = require('./config').SERVER_HOST;

exports.handler = async (event, context, callback) => {

  // Create reusable transporter object
  let transporter = nodemailer.createTransport({
        service: 'Gmail',
        auth: {
            user: adminEmail.username,
            pass: adminEmail.password
        }
  });

  // Setup email data with unicode symbols
  let mailOptions = {
    from: "WayStream <" + adminEmail.username + ">",
    to: event.email,
    subject: "Account Confirmation",
    text: "Hello world?",
    html: "<p>Hello " + event.username + ",</p>" +
              "<p style='margin-left: 20px'>Thanks for signing up for WayStream.</p>" +
              "<p style='margin-left: 20px'>Please click on the following verify address to activate your account: </p>" +
              "<p style='margin-left: 20px'>Email: <span style='margin-left: 100px'>" + event.email + "</span></p>" +
              "<p style='margin-left: 20px'>Verify: <span style='margin-left: 100px'><a href='" + serverHostname + "/confirmEmail/?request=confirm_email&accountID=" + event.account_id + "'>http://waystream.co/verify_email</a></span></p>" +
              "<p style='margin-left: 20px'>If you haven't already, install our app for <span style='color: #15c'>Android</span></p>" +
              "<p style='margin-left: 20px'>If you have any questions, please <span style='color: #15c'>Contact Us</span>.</p>" +
              "<p>Sincerely,</p>" +
              "<p style='font-size: 90%;'>The WayStream Team</p>"
  };

  // Send mail with defined transport object
  let info = await transporter.sendMail(mailOptions)
  
  const response = {
      statusCode: -1,
      body: JSON.stringify('-1')
  };
  if (info.accepted[0] == event.email) {
      response.statusCode = 200;
      response.body = "Email successfully sent";
  }
  else {
      response.statusCode = 409;
      response.body = "Unknown error has occured, debug info: " + info;
  }

  return response;
}