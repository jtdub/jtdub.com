document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const query = params.get("q");
    const resultsContainer = document.getElementById("search-results");

    if (!query) {
        resultsContainer.innerHTML = "<p>Please enter a search query.</p>";
        return;
    }

    // Fetch search data
    fetch("/search.json")
        .then((response) => response.json())
        .then((data) => {
            // Initialize Lunr.js
            const idx = lunr(function () {
                this.field("title");
                this.field("content");
                this.ref("id");

                data.forEach((doc) => {
                    this.add(doc);
                });
            });

            // Perform search
            const results = idx.search(query);
            let output = `<p>Results for "<strong>${query}</strong>":</p><ul>`;

            results.forEach((result) => {
                const item = data.find((doc) => doc.id === result.ref);
                if (item) {
                    output += `
                        <li>
                            <a href="${item.url}">${item.title}</a>
                            <p><small>${item.date}</small></p>
                        </li>
                    `;
                }
            });

            output += "</ul>";
            resultsContainer.innerHTML = results.length > 0 ? output : `<p>No results found for "<strong>${query}</strong>".</p>`;
        })
        .catch((err) => {
            console.error("Error fetching search data:", err);
            resultsContainer.innerHTML = "<p>Error loading search results.</p>";
        });
});
