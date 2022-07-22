let page =0;
let tbody = document.querySelector("#most_rated_shows");
let column = "rating";
let order = "DESC";

async function init() {
    let shows = await getData(page, column, order);
    createPagination();
    updateTable(shows);
    sortHeaders();
}


function sortHeaders() {
    let headers = document.querySelectorAll("th")
    for (let i = 0; i < 4; i++) {
        headers[i].addEventListener("click", async () => {
            headers.forEach((header) => {
                header.classList.remove("headerSortUp", "headerSortDown")
            })
            column = headers[i].textContent.toLowerCase()
            order = order === "DESC" ? "ASC" : "DESC"
            if (order === "DESC") {
                headers[i].classList.add("headerSortDown")
            } else {
                headers[i].classList.add("headerSortUp")
            }
            let shows = await getData(page, column, order);
            updateTable(shows);
        })
    }
}

async function getData(page, column, order) {
    let offset = page * 15;
    let response = await fetch(`/send-most-rated-shows/${offset}/${column}/${order}`);
    return await response.json()
}


function updateTable(shows) {
    tbody.innerHTML = "";
    for (let show of shows) {
        let trailer = show.trailer !== null ? `<a href=${show.trailer} target="blank">${show.trailer}</a>`: "There is no URL"
        let homepage = show.homepage !== null ? `<a href=${show.homepage} target="blank">${show.homepage}</a>`: "There is no URL"
        let link = `<a href='/show/${show.id}'>${show.title}</a>`
        let date = new Date(show.year)
        tbody.innerHTML += `<tr>
                        <td>${link}</td>
                        <td>${date.getFullYear()}</td>
                        <td>${show.runtime}</td>
                        <td>${show.rating}</td>
                        <td>${show.genres}</td>
                        <td>${trailer}</td>
                        <td>${homepage}</td>
                        </tr>`
    }
}


function pages(pagination, minusNum, plusNum) {
    for (let i = page - minusNum; i < page + plusNum; i++) {
        if (i > 67) {
            break
        }

        let num = document.createElement("button");
        num.textContent = i + 1;

        if (i === page) {
            num.style.backgroundColor = "yellow";
            num.style.fontWeight = "bold"
        }

        num.addEventListener("click", async () => {
            page = i;
            let shows = await getData(page);
            updateTable(shows);
            createPagination();
        })
        pagination.appendChild(num)
    }
}


function createPagination() {
    let pagination = document.querySelector("#pagination");
    pagination.innerHTML = "";

    let previous = document.createElement("button");
    let next = document.createElement("button");

    previous.textContent = "«";
    next.textContent = "»";


    previous.addEventListener("click", async () => {
        if (page > 0) {
            page--;
            let shows = await getData(page);
            updateTable(shows);
            createPagination();
        }
    })

    next.addEventListener("click", async () => {
        if (page < 65) {
            page++;
            let shows = await getData(page, column, order);
            updateTable(shows);
            createPagination();
        }
    })

    pagination.appendChild(previous);

    if (page > 1 && page < 5) {
        pages(pagination, 2, 3)
    } else if (page >= 64) {
        pages(pagination, page-63, 5)
    } else {
        pages(pagination, page, 5 - page)
    }

    pagination.appendChild(next);

}

init()

