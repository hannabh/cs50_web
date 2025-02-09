document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Send email if form is submitted
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Query API for emails in mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Display emails on the page
      emails.forEach(email => {
        // Create a new div element with email information
        const mailbox_item = document.createElement('div');
        mailbox_item.id = 'mailbox-item';

        const sender = document.createElement('span');
        sender.id = 'sender';
        sender.textContent = email.sender;
        const subject = document.createElement('span');
        subject.id = 'subject'
        subject.textContent = email.subject;
        const timestamp = document.createElement('span');
        timestamp.id = 'timestamp'
        timestamp.textContent = email.timestamp;

        mailbox_item.appendChild(sender);
        mailbox_item.appendChild(subject);
        mailbox_item.appendChild(timestamp);

        // Add new div to emails-view
        document.querySelector('#emails-view').append(mailbox_item);
      })
  });
}

function send_email(event) {

  // Prevent default form submission
  event.preventDefault();

  let recipients = document.querySelector('#compose-recipients').value;
  let subject = document.querySelector('#compose-subject').value;
  let body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
      // Load sent mailbox
      load_mailbox('sent')
  })
  // Catch any errors and log them to the console
  .catch(error => {
    console.log('Error:', error);
});
}