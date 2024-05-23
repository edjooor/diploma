let earthquakesJS = document.getElementById("earthquake_data").innerText;;
earthquakesJS = earthquakesJS.replaceAll('(', '[');
earthquakesJS = earthquakesJS.replaceAll(')', ']');
earthquakesJS = earthquakesJS.replaceAll("'", '"');
let jsonEarth = JSON.parse(earthquakesJS.replace(/None/g, 'null'));
console.log(jsonEarth);

function draw() {
    var canvas = document.getElementById("canvas");
      var ctx = canvas.getContext("2d");
      len = 315
  
      
      len_step = 50 / 90;
      fall_angle = 5 
      fall_angle_step = 25 / 90
      ctx.beginPath();
      ctx.moveTo(10, 10);
      ctx.lineTo(25, 10);
      ctx.lineTo(25, 16);
      ctx.lineTo(20, 26);
      ctx.lineTo(20, 20);
      ctx.lineTo(250, 100);
      ctx.moveTo(200, 200);
      ctx.lineTo(50, 200);
      ctx.lineTo(100, 100);
      ctx.moveTo(50, 200);
      if (fall_angle == 0 || fall_angle == 90) {
        ctx.lineTo(50, 265);
        ctx.lineTo(200, 265)
      }
      else {
        ctx.moveTo(200, 265)
        ctx.lineTo(200 - fall_angle_step * (90 - fall_angle), len - len_step * (fall_angle))
  
  
        ctx.moveTo(50, 200);
        ctx.lineTo(50 - fall_angle_step * (90 - fall_angle), len - len_step * (fall_angle));
        ctx.lineTo(200 - fall_angle_step * (90 - fall_angle), len - len_step * (fall_angle));
        ctx.lineTo(200, 200);
        ctx.moveTo(200 - fall_angle_step * (90 - fall_angle), len - len_step * (fall_angle));
        ctx.lineTo(150, len - len_step * (fall_angle));
  
      }
  
      ctx.stroke();
      ctx.closePath();
  
  
      
      ctx.beginPath();
      ctx.arc(650, 150, 50, 0, Math.PI * 2, true); // Внешняя окружность
      
      ctx.moveTo(650, 100);
      if (fall_angle == 90) {
        ctx.lineTo(650, 200);
      }
      ctx.closePath();
      ctx.stroke();
  
    }
    draw()
  