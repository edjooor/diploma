let ert = document.getElementById("earthquake_data").innerText;
console.log(ert);
// let earthquakesJS = `{{ earthquakes_S1|safe }}`;
// earthquakesJS = earthquakesJS.replaceAll('(', '[');
// earthquakesJS = earthquakesJS.replaceAll(')', ']');
// earthquakesJS = earthquakesJS.replaceAll("'", '"');
// let jsonEarth = JSON.parse(earthquakesJS.replace(/None/g, 'null'));
// console.log(jsonEarth);



// const width = window.innerWidth * 0.6;
// const height = Math.min(width, 720);
// const canvas = document.getElementById("globe");
// const dpr = window.devicePixelRatio || 1;
// canvas.width = dpr * width;
// canvas.height = dpr * height;
// canvas.style.width = `${width}px`;
// const context = canvas.getContext("2d");
// context.scale(dpr, dpr);

// let projection = d3.geoOrthographic()
//     .fitExtent([[10, 10], [width - 10, height - 10]], { type: "Sphere" });
// const path = d3.geoPath(projection, context);
// const tooltip = d3.select("#tooltip");

// // Example points data
// let points = [{ coordinates: [0, 1], name: "", date: "" }];



// for (let i = 0; i < jsonEarth.length; ++i) {
//     points[i] = { coordinates: [Number(jsonEarth[i][4]), Number(jsonEarth[i][3])], name: "fjf", date: jsonEarth[i][1] };
// }
// console.log(points)




// // Fetch data and initialize the visualization
// Promise.all([
//     d3.json("https://d3js.org/world-110m.v1.json"),
// ]).then(([worldData]) => {
//     const land = topojson.feature(worldData, worldData.objects.land);
//     const borders = topojson.mesh(worldData, worldData.objects.countries, (a, b) => a !== b);

//     function render() {
//         context.clearRect(0, 0, width, height);
//         context.beginPath(), path(land), context.fillStyle = "#ccc", context.fill();
//         context.beginPath(), path(borders), context.strokeStyle = "#fff", context.lineWidth = 0.5, context.stroke();
//         context.beginPath(), path({ type: "Sphere" }), context.strokeStyle = "#000", context.lineWidth = 1.5, context.stroke();

//         // Render points
//         points.forEach(point => {
//             const [x, y] = projection(point.coordinates);
//             if (isVisible(point.coordinates)) {
//                 context.beginPath();
//                 context.arc(x, y, 3, 0, 2 * Math.PI);
//                 context.fillStyle = "#f00";
//                 context.fill();
//                 context.strokeStyle = "#000";
//                 context.stroke();
//             }
//         });
//     }

//     function isVisible(coordinates) {
//         const [x, y] = projection(coordinates);
//         const center = projection.invert([width / 2, height / 2]);
//         const distance = d3.geoDistance(center, coordinates);
//         return distance < Math.PI / 2;
//     }

//     // Mouse event listeners for rotation
//     let isDragging = false;
//     let lastX, lastY;

//     canvas.addEventListener("mousedown", function (event) {
//         isDragging = true;
//         lastX = event.clientX;
//         lastY = event.clientY;
//     });

//     canvas.addEventListener("mousemove", function (event) {
//         if (isDragging) {
//             const dx = event.clientX - lastX;
//             const dy = event.clientY - lastY;
//             const rotate = projection.rotate();
//             const sensitivity = 0.25;

//             projection.rotate([
//                 rotate[0] + dx * sensitivity,
//                 rotate[1] - dy * sensitivity
//             ]);

//             lastX = event.clientX;
//             lastY = event.clientY;
//             render();
//         }

//         const [mouseX, mouseY] = [event.clientX, event.clientY];
//         const [x, y] = [mouseX - canvas.getBoundingClientRect().left, mouseY - canvas.getBoundingClientRect().top];
//         const inverted = projection.invert([x, y]);

//         let found = false;
//         points.forEach(point => {
//             const [px, py] = projection(point.coordinates);
//             const distance = Math.sqrt((x - px) ** 2 + (y - py) ** 2);
//             if (distance < 5) {
//                 tooltip.style("opacity", 1)
//                     .style("left", `${mouseX + 5}px`)
//                     .style("top", `${mouseY + 5}px`)
//                     .html(`<strong>${point.name} <br/> Координаты: ${point.coordinates} <br/> Дата: ${point.date}</strong>`);
//                 found = true;
//             }
//         });

//         if (!found) {
//             tooltip.style("opacity", 0);
//         }
//     });

//     canvas.addEventListener("mouseup", function () {
//         isDragging = false;
//     });

//     canvas.addEventListener("mouseout", function () {
//         isDragging = false;
//         tooltip.style("opacity", 0);
//     });

//     // Zoom controls
//     document.getElementById("zoomIn").addEventListener("click", function () {
//         zoom(1.1);
//     });

//     document.getElementById("zoomOut").addEventListener("click", function () {
//         zoom(0.9);
//     });

//     function zoom(scaleFactor) {
//         const scale = projection.scale() * scaleFactor;
//         projection = projection.scale(scale);
//         render();
//     }

//     render();
// });