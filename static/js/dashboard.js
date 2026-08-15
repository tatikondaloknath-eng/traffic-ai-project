const optimizeButton =
    document.getElementById("optimizeButton");


optimizeButton.addEventListener(
    "click",
    function () {

        optimizeButton.innerText =
            "AI Optimization Running...";

        optimizeButton.disabled = true;


        setTimeout(function () {

            optimizeButton.innerText =
                "Optimization Complete ✓";

            optimizeButton.disabled = false;

        }, 2000);

    }
);
