let searchForm = document.getElementById("searchForm");
let pageLink = document.getElementsByClassName("page-link");
// console.log(pageLink);

if (searchForm) {
  for (let i = 0; i < pageLink.length; i++) {
    pageLink[i].addEventListener("click", function (e) {
      e.preventDefault();

      // Get the data value
      let page = this.dataset.page;
      // Add hidden search input
      searchForm.innerHTML += `<input value=${page} name="page" hidden />`;

      // Submit form
      searchForm.submit();
    });
  }
}
// Remove tags from a project
const tags = document.getElementsByClassName("project-tag");
for (let i = 0; i < tags.length; i++) {
  tags[i].addEventListener("click", async (e) => {
    e.preventDefault();
    const tagId = e.target.dataset.tag;
    const projectId = e.target.dataset.project;

    const response = await axios.delete(
      "http://localhost:8000/api/remove-tag/",
      {
        Headers: {
          "Content-Type": "application/json",
        },
        data: {
          tag: tagId,
          project: projectId,
        },
      }
    );
    if (response.data) {
      e.target.remove();
    }
  });
}
