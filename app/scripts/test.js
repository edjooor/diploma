// Инициализация карты
function initMap() {
    // Создание новой карты с центром и начальным масштабом
    var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 52.5200, lng: 13.4050 }, // Начальные координаты центра карты [широта, долгота]
        zoom: 10 // Начальный уровень масштабирования
    });

    // Создание массива маркеров
    var markers = [
        { position: { lat: 52.5200, lng: 13.4050 }, title: 'Berlin' }, // Маркер 1
        { position: { lat: 52.52, lng: 13.39 }, title: 'Potsdamer Platz' }, // Маркер 2
        { position: { lat: 52.52, lng: 13.40 }, title: 'Brandenburger Tor' } // Маркер 3
    ];

    // Добавление маркеров на карту
    markers.forEach(function(markerInfo) {
        var marker = new google.maps.Marker({
            position: markerInfo.position,
            map: map,
            title: markerInfo.title
        });

        // Добавление события клика на маркер
        marker.addListener('click', function() {
            alert('Вы кликнули на маркере: ' + markerInfo.title);
            // Можно выполнить другие действия, связанные с местом клика
        });
    });
}