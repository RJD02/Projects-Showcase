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
