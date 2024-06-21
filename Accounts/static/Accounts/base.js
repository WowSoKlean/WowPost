document.addEventListener("DOMContentLoaded", function() {
  const posts = document.querySelectorAll('.card');
  let currentPage = 1;
  const postsPerPage = 2;  

  function showPosts(pageNumber) {
    const startIndex = (pageNumber - 1) * postsPerPage;
    const endIndex = Math.min(startIndex + postsPerPage, posts.length);

    for (let i = 0; i < posts.length; i++) {
      posts[i].style.display = 'none';
    }

    for (let i = startIndex; i < endIndex; i++) {
      posts[i].style.display = 'block';
    }

    updateButtonStates(pageNumber);
  }

  function updateButtonStates(pageNumber) {
    const prevButton = document.getElementById('prevButton');
    const nextButton = document.getElementById('nextButton');

    prevButton.disabled = pageNumber === 1;
    nextButton.disabled = pageNumber === Math.ceil(posts.length / postsPerPage);
  }

  showPosts(currentPage);  

  nextButton.addEventListener('click', () => {
    currentPage++;
    showPosts(currentPage);
  });

  prevButton.addEventListener('click', () => {
    currentPage--;
    showPosts(currentPage);
  });
});


