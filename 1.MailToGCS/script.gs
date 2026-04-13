// Replace with your bucket name
const BUCKET_NAME = 'ecomm-bucket';

function saveGmailAttachmentToGCS() {
  // Search for the specific email (e.g., from a specific sender with a subject)
  const threads = GmailApp.search('from:reports@example.com subject:"Daily Sales" has:attachment');
  const message = threads[0].getMessages().pop(); // Get the latest email
  const attachment = message.getAttachments()[0]; // Get the first attachment

  // Use the GCS API to upload the blob
  // Note: You'll need to enable the "Cloud Storage" advanced service or use an HTTP fetch
  UrlFetchApp.fetch(`https://storage.googleapis.com/upload/storage/v1/b/${BUCKET_NAME}/o?uploadType=media&name=orders_raw.csv`, {
    method: 'POST',
    contentType: 'text/csv',
    payload: attachment.copyBlob(),
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() }
  });
}