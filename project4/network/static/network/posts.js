function savePost(postContentWrapper) {
    alert('saving post')  // TODO
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-link').forEach(link => {
        link.onclick = (event) => {

            // prevent link from reloading page
            event.preventDefault() 

            // Find the post content of the clicked edit link
            let postContentWrapper = event.target.closest('.post-content-wrapper');
            let postContent = postContentWrapper.querySelector('.post-content');

            // replace post content with textarea and Save button
            postContentWrapper.innerHTML = `
            <textarea id="edit-text" class="form-control" rows="3">${postContent.textContent}</textarea>
            <button class="btn btn-primary" id="save-button">Save</button>
            `;

            // add event listener for Save button
            postContentWrapper.querySelector('#save-button').onclick = savePost;
        }
    });
});
