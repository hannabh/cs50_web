function editPost(postContentWrapper) {
    let postContent = postContentWrapper.querySelector('.post-content');

    // replace post content with textarea and Save button
    postContentWrapper.innerHTML = `
    <textarea id="edit-text" class="form-control" rows="3">${postContent.textContent}</textarea>
    <button class="btn btn-primary" id="save-button">Save</button>
    `;
    // add event listener to Save button
    postContentWrapper.querySelector('#save-button').addEventListener('click', function() {
        savePost(postContentWrapper);
    });
}

function savePost(postContentWrapper) {
    // TODO: actually update post using API

    let editedContent = postContentWrapper.querySelector('#edit-text').value;

    postContentWrapper.innerHTML = `
    <p class="post-content">${editedContent}</p>
    <a class="edit-link" href="#">Edit</a>
    `

    // reattach event listener for the new edit link
    postContentWrapper.querySelector('.edit-link').addEventListener('click', function(event) {
        event.preventDefault();
        editPost(postContentWrapper);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.edit-link').forEach(link => {
        link.onclick = (event) => {

            // prevent link from reloading page
            event.preventDefault() 

            // find the post content wrapper of the clicked edit link
            let postContentWrapper = event.target.closest('.post-content-wrapper');

            editPost(postContentWrapper);
        }
    });
})
