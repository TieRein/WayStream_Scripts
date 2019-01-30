/* Author: Jacob Chesley
*
*  Node.js script to send confirmation emails
*  In development and not currently usable
*
*  Code template utilized from E4R Junior Project
*  https://github.com/TieRein/e4r-1
*
*  Last Updated: 1/30/19
*/

const nodemailer = require('nodemailer');
const adminEmail = require('./config').Email_Config;
const serverHostname = require('./config').Server_Host;

exports.handler = async (event) => {
    console.log(event);
    
    var transporter = nodemailer.createTransport({
            service: 'Gmail',
            auth: {
                user: adminEmail.username,
                pass: adminEmail.password
            }
    });
    let HelperOptions = {
        from: "WayStream <" + adminEmail.username + ">",
        to: event.email,
        subject: "Account Confirmation",
        html: "<p>Hello " + event.username + ",</p>" +
              "<p style='margin-left: 20px'>Thanks for signing up for WayStream.</p>" +
              "<p style='margin-left: 20px'>Please click on the following verify address to activate your account: </p>" +
              "<p style='margin-left: 20px'>Email: <span style='margin-left: 100px'>" + event.email + "</span></p>" +
              "<p style='margin-left: 20px'>Verify: <span style='margin-left: 100px'><a href='" + serverHostname + "/api/verify_email/" + id + "'>http://waystream.co/verify_email</a></span></p>" +
              "<p style='margin-left: 20px'>If you haven't already, install our app for <span style='color: #15c'>Android</span></p>" +
              "<p style='margin-left: 20px'>If you have any questions, please <span style='color: #15c'>Contact Us</span>.</p>" +
              "<p>Sincerely,</p>" +
              "<p style='font-size: 90%;'>The WayStream Team</p>"
    };
    transporter.sendMail(HelperOptions, (err, response)=>{
        if(err) {
            console.log('Confirmation Email failed: ' + event.email);
            return false;
        }
    });
    console.log("Confirmation Email Sent: " + event.email);
    
    const response = {
        statusCode: 200,
        body: JSON.stringify('Hello from Lambda!'),
    };
    return response;
};
