const BASE_URL = "http://localhost:5000/api";

// select elements(cupcakeList, newCupcakeForm)
const cupcakesList = document.querySelector("#cupcake-list");
const newCupcakeForm = document.querySelector("#new-cupcake-form");

// add cupcakes to the list
function addCupcake(cupcake) {
    const newCupcakeImage = document.createElement("img");
    newCupcakeImage.src = cupcake.image;
    const newCupcake = document.createElement("li");
    newCupcake.innerText = `${cupcake.flavor} - ${cupcake.size} - ${cupcake.rating}`;
    newCupcake.prepend(newCupcakeImage);
    cupcakesList.append(newCupcake);
}

// get all cupcakes from the API
async function getCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    for (let cupcake of response.data.cupcakes) {
        addCupcake(cupcake);
    }
}

// submit new cupcake form
newCupcakeForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const flavor = document.querySelector("#flavor").value;
    const size = document.querySelector("#size").value;
    const rating = document.querySelector("#rating").value;
    const image = document.querySelector("#image").value;
    const response = await axios.post(`${BASE_URL}/cupcakes`, { flavor, size, rating, image });
    addCupcake(response.data.cupcake);
});

// get all cupcakes when the page loads
getCupcakes();

