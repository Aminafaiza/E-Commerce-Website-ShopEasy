
// ShopEasy Main JavaScript

document.addEventListener("DOMContentLoaded", function () {

    // Smooth scrolling for section links
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {

        link.addEventListener("click", function (event) {

            const targetId = this.getAttribute("href");

            if (targetId && targetId.length > 1) {

                const target = document.querySelector(targetId);

                if (target) {
                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth"
                    });
                }
            }

        });

    });


    // Prevent empty product searches
    const searchForm = document.querySelector(".search-form");

    if (searchForm) {

        searchForm.addEventListener("submit", function (event) {

            const searchInput = searchForm.querySelector(
                'input[name="q"]'
            );

            if (!searchInput.value.trim()) {
                event.preventDefault();
                searchInput.focus();
            }

        });

    }

});
