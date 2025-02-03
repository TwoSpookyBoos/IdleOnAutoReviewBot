BONUS_CLASSES = [
        'static/imgs/wiki/Animal_Farm_Lab_Bonus.png',
        'static/imgs/wiki/Wired_In_Lab_Bonus.png',
        'static/imgs/wiki/Gilded_Cyclical_Tubing_Lab_Bonus.png',
        'static/imgs/wiki/No_Bubble_Left_Behind_Lab_Bonus.png',
        'static/imgs/wiki/Killer%27s_Brightside_Lab_Bonus.png',
        'static/imgs/wiki/Shrine_World_Tour_Lab_Bonus.png',
        'static/imgs/wiki/Viaduct_of_the_Gods_Lab_Bonus.png',
        'static/imgs/wiki/Certified_Stamp_Book_Lab_Bonus.png',
        'static/imgs/wiki/Spelunker_Obol_Lab_Bonus.png',
        'static/imgs/wiki/Fungi_Finger_Pocketer_Lab_Bonus.png',
        'static/imgs/wiki/My_1st_Chemistry_Set_Lab_Bonus.png',
        'static/imgs/wiki/Unadulterated_Banking_Fury_Lab_Bonus.png',
        'static/imgs/wiki/Sigils_of_Olden_Alchemy_Lab_Bonus.png',
        'static/imgs/wiki/Viral_Connection_Lab_Bonus.png',
        'static/imgs/wiki/Artifact_Attraction_Lab_Bonus.png',
        'static/imgs/wiki/Slab_Sovereignty_Lab_Bonus.png',
        'static/imgs/wiki/Spiritual_Growth_Lab_Bonus.png',
        'static/imgs/wiki/Depot_Studies_PhD_Lab_Bonus.png'
]

waitForElm("#labCanvas").then(canvas => {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    createAndDrawBackground(ctx, canvas.width, canvas.height).then(() => {
        ctx.strokeStyle = "black";
        for(const [x, y] of eval(canvas.getAttribute("data-characters"))) {
            ctx.fillRect(x-15, y-15, 30, 30); 
        }
        const jewels = eval(canvas.getAttribute("data-jewels"));
        for(const i in jewels) {
            createAndDrawCenteredImg(ctx, `static/imgs/customized/Console_Jewel_${i}.png`, ...jewels[i], 60, 60)
        }
        const bonuses = eval(canvas.getAttribute("data-bonuses"));
        for(const i in bonuses) {
            createAndDrawCenteredImg(ctx, BONUS_CLASSES[i], ...bonuses[i], 60, 60)
        }
    })
})

function createAndDrawCenteredImg(ctx, src, x, y, width, height) {
    const img = new Image();
    img.src = src;
    img.onload = () => { // Ensure the image is drawn only after it loads
        ctx.drawImage(img, (x-width/2), (y-height/2), width, height);
    };
}

function createAndDrawImg(ctx, src, x, y, width, height) {

}

function createAndDrawBackground(ctx, width, height) {
    const loadImage = (src) => {
        return new Promise((resolve) => {
            const img = new Image();
            img.src = src;
            img.onload = () => resolve(img);
        });
    };

    const drawBackground = async () => {
        // Load all images in parallel
        const [leftImg, centerImg, rightImg] = await Promise.all([
            loadImage('static/imgs/lab/lab-background-left.png'),
            loadImage('static/imgs/lab/lab-background-center.png'),
            loadImage('static/imgs/lab/lab-background-right.png')
        ]);

        // Draw left image
        const leftRatio = height / leftImg.height;
        ctx.drawImage(leftImg, 0, 0, leftImg.width * leftRatio, height);

        // Draw right image
        const rightRatio = height / rightImg.height;
        const rightX = width - rightImg.width * rightRatio;
        ctx.drawImage(rightImg, rightX, 0, rightImg.width * rightRatio, height);

        // Draw center image
        const centerX = leftImg.width * leftRatio;
        const centerWidth = width - (leftImg.width * leftRatio + rightImg.width * rightRatio);
        ctx.drawImage(centerImg, centerX, 0, centerWidth, height);
    };

    return drawBackground();
}



function waitForElm(selector) {
    return new Promise(resolve => {
        if (document.querySelector(selector)) {
            return resolve(document.querySelector(selector));
        }

        const observer = new MutationObserver(mutations => {
            if (document.querySelector(selector)) {
                observer.disconnect();
                resolve(document.querySelector(selector));
            }
        });

        // If you get "parameter 1 is not of type 'Node'" error, see https://stackoverflow.com/a/77855838/492336
        observer.observe(document.body || document.documentElement, {
            childList: true,
            subtree: true
        });
    });
}