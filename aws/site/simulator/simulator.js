var Tester, Holder, Bs;
var larmor_slider, delta_w_slider;
var larmor_label, delta_w_label;

function init() {
    Holder = document.getElementById("holder"); 
    TESTER = document.getElementById('tester');
    larmor_slider = document.getElementById("larmor");
    delta_w_slider = document.getElementById("delta_w");

    larmor_label = document.getElementById("larmor_label");
    delta_w_label = document.getElementById("delta_w_label");

    Bs = linspace(0, 400, 8);

    Plotly.plot( TESTER, dummy(Bs, -9.2, -8.1, 300),{  
        margin: { t: 0 },xaxis:{range: [-9.2, -8.1]},
        showlegend: false }, 
        {staticPlot: true,
        responsive: true} );
    
    update();
    resize_plot();
}

function resize_plot() {
    console.log("resize");
    // Plotly.relayout(TESTER, {
    //     width: 0.9 * TESTER.clientWidth,
    //     height: 0.9 * TESTER.clientHeight
    //   })
}

window.onresize = function(event) {
    resize_plot()
  }

function dummy(Bs, lower, upper, steps) {
    data = []
    for (var i = 0; i < Bs.length*2; i++) {
        grouper = i - (i % 2);
        col = "rgb(0,0," + 255 * (grouper/(Bs.length*2)) + ")";
        data.push({
            x: linspace(lower, upper, steps),
            y: linspace(lower, upper, steps).map(x => Math.pow(x, 1+(i/(Bs.length*2)))),
            marker: {
                color: col
            }
        })
    }
    return data
}

function update() {
    larmor_label.innerHTML = larmor.value;
    delta_w_label.innerHTML = delta_w.value;
    new_data = gen_data(Bs, 
        200,
        100,
        100,
        7,
        20,
        14,
        larmor_slider.value,
        delta_w_slider.value);
	Plotly.restyle(TESTER, "y", new_data);
}

function cauchy(x,x0,fwhm) {
    gamma = fwhm/2
    return 1/ (  Math.PI*(gamma/2) * (1 + Math.pow(((x-x0)/gamma),2)) );
}

function norm_cauchy(x,x0,fwhm) {
    gamma = fwhm/2
    return 1/ (  Math.PI*(gamma/2) * (1 + Math.pow(((x-x0)/gamma), 2)) ) * Math.PI * gamma / 2;
}

function y_vals(A, B, Kd, koff, dR2, mw, lw, sw, larmor, delta_w) {
  AB = ( (A + B + Kd) - Math.sqrt( Math.pow((A + B + Kd), 2) - 4*A*B ) ) / 2
  pb = AB/A
  pa = 1 - pb
  
  //Assume 1:1 stoichiometry
  kr = koff
  B_free = B - AB
  kon = koff/Kd
  kf = kon*B_free
  kex = kr + kf
  
  broad_denom = Math.pow(Math.pow(kex, 2) + (1-5*pa*pb)*Math.pow(delta_w, 2), 2) + 4*pa*pb*(1-4*pa*pb)*Math.pow(delta_w,4)

  lw_broad = pa*pb*Math.pow(delta_w,2)*kex * (Math.pow(kex, 2)+(1-5*pa*pb)*Math.pow(delta_w, 2))/broad_denom
  lw_obs = (pa*lw + pb*(lw+dR2) + lw_broad) 
  
  cs_broad = pa*pb*(pa-pb)*Math.pow(delta_w,3) * (Math.pow(kex, 2)+(1-3*pa*pb)*Math.pow(delta_w, 2))/broad_denom
  cs_shift = pb*delta_w - cs_broad
  line1 = sw.map(x => cauchy(x, -9, (pa*lw + pb*(lw+dR2))/larmor));
  line2 = sw.map(x => cauchy(x, -8.6 + cs_shift/larmor, lw_obs/larmor));
  return [line1, line2]
}

function gen_data(Bs, A, Kd, koff, dR2, mw, lw, larmor, delta_w) {
    res = []
    sw = linspace(-9.2, -8.1, 300);
    for (var i = 0; i < Bs.length; i++) {
        B = Bs[i];
        vals = y_vals(A,
            B,
            Kd,
            koff,
            dR2,
            mw,
            lw,
            sw,
            larmor,
            delta_w);
        res.push(...vals);
    }
    return res;
}

function linspace(start, stop, steps) {
    step_size = (stop - start) / (steps - 1);
    arr = [];
    for (var i = start; i <= stop; i+=step_size) {
        arr.push(i);
    }
    return arr;
}