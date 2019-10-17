const items = document.getElementsByClassName('select_rest');
const nearItems = document.getElementsByClassName('select_near');

for (let i = 0; i < items.length; i++) {
    items[i].onclick = () => {
        document.getElementById('name').innerHTML = items[i].getAttribute("data-name");
        document.getElementById('address').innerHTML = items[i].getAttribute("data-address");
        document.getElementById('cuisines').innerHTML = items[i].getAttribute("data-cuisine");
        document.getElementById('raiting').innerHTML = items[i].getAttribute("data-rate");
        document.getElementById('photo').src = items[i].getAttribute("data-photo");
    }
}

for (let i = 0; i < nearItems.length; i++) {
    nearItems[i].onclick = () => {
        document.getElementById('route').src = nearItems[i].getAttribute("data-route");
    }
}