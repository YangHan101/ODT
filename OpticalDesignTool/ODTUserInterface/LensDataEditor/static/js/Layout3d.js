var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(45, parent.innerWidth/parent.innerHeight, 1, 1000);
camera.position.set(0, 0, 250);

var light = []
light[0] = new THREE.DirectionalLight(0xFFFFFF, 1.0);
light[0].position.set(0,-100,100);
scene.add(light[0]);

light[1] = new THREE.DirectionalLight(0xFFFFFF, 1.0);
light[1].position.set(-100, 100, 0);
scene.add(light[1]);

light[2] = new THREE.DirectionalLight(0xFFFFFF, 1.0);
light[2].position.set(100, 0, -100);
scene.add(light[2]);

var cube = new THREE.Object3D();

var lensData = new Object();
lensData = JSON.parse("{{lensData}}".replace(/&quot;/g,'"'));


var accumThickness = 0;

for (var isurf = 0; isurf < lensData.length -1 ; isurf ++)
{
    console.log(isurf);
    console.log(accumThickness);

    if (lensData[isurf].surfaceMaterial !=='Air')
    {
        var lensgeometry = DrawLens(lensData[isurf], lensData[isurf + 1]);
        var material = new THREE.MeshLambertMaterial( { color: matColor[isurf % matColor.length]} );
        var lens = new THREE.Mesh( lensgeometry, material );

        lens.position.z = accumThickness;

        cube.add( lens );
    }

    accumThickness += lensData[isurf].surfaceThickness;

}
cube.rotation.y = Math.PI/2;

scene.add(cube);



var renderer = new THREE.WebGLRenderer();
renderer.setSize( parent.innerWidth/2, parent.innerHeight/2 );
document.body.appendChild( renderer.domElement );
//var container = document.getElementsByClassName( "container" );
//container[0].appendChild( renderer.domElement );

var render = function () {
requestAnimationFrame( render );

cube.rotation.y += 0.01;
renderer.render(scene, camera);
};

render();