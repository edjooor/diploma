let got_id = document.getElementById("earthquake_data_id").innerText;
console.log(got_id);
document.addEventListener("DOMContentLoaded", function() {
    const imageContainer = document.getElementById("image-container");

    // Замените "beachball_1.png" на имя вашего файла
    let path_to = '/static/beachballs/beachball_'+String(got_id) + '.png';
    console.log(path_to)
    const imageUrl = path_to;

    // Создаем элемент изображения
    const imgElement = document.createElement("img");
    imgElement.src = imageUrl;
    imgElement.alt = "Beachball Image";

    // Добавляем изображение в контейнер
    imageContainer.appendChild(imgElement);
});