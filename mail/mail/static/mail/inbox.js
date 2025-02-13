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

function compose_email(recipients='', subject='', body='') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';
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
        // Add 'read' class if the email has been read
        if (email.read) {
          mailbox_item.classList.add('read');
        };

        const sender = document.createElement('span');
        sender.id = 'sender';
        sender.textContent = email.sender;
        const subject = document.createElement('span');
        subject.id = 'subject';
        subject.textContent = email.subject;
        const timestamp = document.createElement('span');
        timestamp.id = 'timestamp';
        timestamp.textContent = email.timestamp;

        mailbox_item.appendChild(sender);
        mailbox_item.appendChild(subject);
        mailbox_item.appendChild(timestamp);

        // Add click event listener to mailbox item
        mailbox_item.addEventListener('click', function() {
          view_email(email.id, mailbox)
        });

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

function view_email(id, mailbox) {
    // Show email content view
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#email-content-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Get email
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        console.log(email);

        // Show email content on page
        document.querySelector('#email-content-view').innerHTML = `
        <p><b>From:</b> ${email.sender}</p>
        <p><b>To:</b> ${email.recipients}</p>
        <p><b>Subject:</b> ${email.subject}</p>
        <p><b>Timestamp:</b> ${email.timestamp}</p>

        <hr>

        <p>${email.body}</p>
        `

        // Add reply button for inbox emails
        if (mailbox == 'inbox') {
          const reply_btn = document.createElement('button');
          reply_btn.textContent = 'Reply';
          reply_btn.className = "btn btn-primary";
          reply_btn.addEventListener('click', () => compose_email(
            recipients=email.sender,
            subject=`Re: ${email.subject}`,
            body=`On ${email.timestamp}, ${email.sender} wrote: ${email.body}`,
          )
        );
          document.querySelector('#email-content-view').append(reply_btn);
        };

        // Add archive button for inbox emails
        if (mailbox == 'inbox') {
          const archive_btn = document.createElement('button');
          archive_btn.textContent = 'Archive';
          archive_btn.className = "btn btn-primary";
          archive_btn.addEventListener('click', () => archive_email(id));
        document.querySelector('#email-content-view').append(archive_btn);
        };

        // Add unarchive button for archive emails
        if (mailbox == 'archive') {
          const unarchive_btn = document.createElement('button');
          unarchive_btn.textContent = 'Unarchive';
          unarchive_btn.className = "btn btn-primary";
          unarchive_btn.addEventListener('click', () => unarchive_email(id));
        document.querySelector('#email-content-view').append(unarchive_btn);
        };
      
        // Mark email as read
        fetch(`/emails/${id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
  });
}

function archive_email(id) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
      })
      .then(response => load_mailbox('inbox'))
}

function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(response => load_mailbox('inbox'))
}