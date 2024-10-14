document.addEventListener('DOMContentLoaded', function() {
    const mapItemsList = document.getElementById('mapItemsList');
    const earthquakes = JSON.parse(mapItemsList.getAttribute('data-earthquakes'));
    const earthquakeDetailUrl = mapItemsList.getAttribute('data-earthquake-detail-url');
    const earthquakeDetailUrl2 = mapItemsList.getAttribute('data-earthquake-detail2-url');


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
        // console.log(earthquakeDetailUrl);


        
        const link2 = document.createElement('a');
        link2.href = earthquakeDetailUrl2 + earthquake[0];
        link2.className = 'moreInfo2';
        link2.textContent = 'Вторые моменты';
        console.log(earthquakeDetailUrl2);

        div.appendChild(link);
        div.appendChild(link2);

        return div;
    }
   
    
    function renderList(sortedEarthquakes) {
        mapItemsList.innerHTML = '';
        sortedEarthquakes.map(createListItem).forEach(listItem => mapItemsList.appendChild(listItem));
    }
    
    function parseDate(dateStr) {
        const [day, month, year] = dateStr.split('.');
        return new Date(year, month - 1, day); 
    }
    
    const minMagnitudeInput = document.getElementById('minMagnitude');
    const maxMagnitudeInput = document.getElementById('maxMagnitude');
    const minDateInput = document.getElementById('minDate');
    const maxDateInput = document.getElementById('maxDate');
    const minDepthInput = document.getElementById('minDepth');
    const maxDepthInput = document.getElementById('maxDepth');
    const sortSelector = document.getElementById('sortSelector');
    
    function filterAndSortEarthquakes() {
        const minMagnitude = parseFloat(minMagnitudeInput.value);
        const maxMagnitude = parseFloat(maxMagnitudeInput.value);
        const minDate = minDateInput.value ? new Date(minDateInput.value) : new Date('1900-01-01');
        const maxDate = maxDateInput.value ? new Date(maxDateInput.value) : new Date();
        const minDepth = parseFloat(minDepthInput.value);
        const maxDepth = parseFloat(maxDepthInput.value);
        const sortBy = sortSelector.value;
    
        let filteredEarthquakes = earthquakes.filter(eq => {
            const magnitude = parseFloat(eq[11]);
            const date = parseDate(eq[1]);
            const depth = parseFloat(eq[13]);
    
            return (
                magnitude >= minMagnitude &&
                magnitude <= maxMagnitude &&
                date >= minDate &&
                date <= maxDate &&
                depth >= minDepth &&
                depth <= maxDepth
            );
        });
    
        let sortedEarthquakes;
        if (sortBy === 'name') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => a[26].localeCompare(b[26]));
        } else if (sortBy === 'datedown') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseDate(b[1]) - parseDate(a[1]));
        } else if (sortBy === 'dateup') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseDate(a[1]) - parseDate(b[1]));
        } else if (sortBy === 'magnitudelow') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseFloat(a[11]) - parseFloat(b[11]));
        } else if (sortBy === 'magnitudehigh') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseFloat(b[11]) - parseFloat(a[11]));
        } else if (sortBy === 'depthlow') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseFloat(a[12]) - parseFloat(b[12]));
        } else if (sortBy === 'depthhigh') {
            sortedEarthquakes = filteredEarthquakes.sort((a, b) => parseFloat(b[12]) - parseFloat(a[12]));
        }
    
        renderList(sortedEarthquakes);
    }
    
    sortSelector.addEventListener('change', filterAndSortEarthquakes);
    minMagnitudeInput.addEventListener('input', filterAndSortEarthquakes);
    maxMagnitudeInput.addEventListener('input', filterAndSortEarthquakes);
    minDateInput.addEventListener('input', filterAndSortEarthquakes);
    maxDateInput.addEventListener('input', filterAndSortEarthquakes);
    minDepthInput.addEventListener('input', filterAndSortEarthquakes);
    maxDepthInput.addEventListener('input', filterAndSortEarthquakes);
    
    filterAndSortEarthquakes();
    
    

});






















