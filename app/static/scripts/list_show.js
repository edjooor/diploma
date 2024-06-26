document.addEventListener('DOMContentLoaded', function() {
    const mapItemsList = document.getElementById('mapItemsList');
    const earthquakes = JSON.parse(mapItemsList.getAttribute('data-earthquakes'));
    const earthquakeDetailUrl = mapItemsList.getAttribute('data-earthquake-detail-url');
    console.log(earthquakes)

    function createListItem(earthquake) {
        const div = document.createElement('div');
        div.id = 'listItem';
        div.innerHTML = `<strong>${earthquake[26]}</strong> <br><p>  <b> Дата:</b> ${earthquake[1]}</p> 
       <p>  <b> Координаты:</b> ${earthquake[3]}, ${earthquake[4]}</p>
        <p>  <b> Mw:</b> ${earthquake[11]}</p>`;
            


        const link = document.createElement('a');
        link.href = earthquakeDetailUrl + earthquake[0];
        link.className = 'moreInfo';
        link.textContent = 'Подробнее';

        div.appendChild(link);

        return div;
    }
   
    
    function renderList(sortedEarthquakes) {
        mapItemsList.innerHTML = '';
        sortedEarthquakes.map(createListItem).forEach(listItem => mapItemsList.appendChild(listItem));
    }

    const sortedEarthquakes = [...earthquakes].sort((a, b) => a[26].localeCompare(b[26]));
    const sortSelector = document.getElementById('sortSelector');
    sortSelector.addEventListener('change', function() {
        const sortBy = sortSelector.value;
        function parseDate(dateStr) {
            const [day, month, year] = dateStr.split('.');
            return new Date(year, month - 1, day); 
        }
        let sortedEarthquakes;
        if (sortBy === 'name') {
            sortedEarthquakes = [...earthquakes].sort((a, b) => a[26].localeCompare(b[26]));
        } else if (sortBy === 'datedown') {
            sortedEarthquakes = [...earthquakes].sort((a, b) => parseDate(b[1]) - parseDate(a[1]));
        }
        else if (sortBy === 'dateup') {
            sortedEarthquakes = [...earthquakes].sort((a, b) => parseDate(a[1]) - parseDate(b[1]));
        }
        else if (sortBy === 'magnitudelow') {
            sortedEarthquakes = [...earthquakes].sort((a, b) => parseFloat(a[11]) - parseFloat(b[11]));
        }
        else if (sortBy === 'magnitudehigh') {
            sortedEarthquakes = [...earthquakes].sort((a, b) => parseFloat(b[11]) - parseFloat(a[11]));
        }
        renderList(sortedEarthquakes);
    });

    
    renderList(sortedEarthquakes);

});






















