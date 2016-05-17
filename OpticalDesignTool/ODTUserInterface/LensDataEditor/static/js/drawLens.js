function computeZ(x, y, c, k)
{
    var r = Math.pow(Math.pow(x, 2) + Math.pow(y, 2), 0.5);
    var z = c * Math.pow(r,2) / (1 + Math.pow( Math.max(0, 1 - (1 + k) * Math.pow(c * r , 2)) , 0.5) );
    return z;
}



function DrawLens(surf1, surf2)
{
    var ntheta = 48;
    var nrad = 12;

    c1 = surf1.surfaceVertexCurvature;
    dx1 = surf1.surfaceDecenterX;
    dy1 = surf1.surfaceDecenterY;
    k1 = surf1.surfaceConicConstant;

    c2 = - surf2.surfaceVertexCurvature;
    dx2 = surf2.surfaceDecenterX;
    dy2 = surf2.surfaceDecenterY;
    k2 = surf2.surfaceConicConstant;

    var lens = new THREE.Geometry();

    var x = 0;
    var y = 0;
    var point = new THREE.Vector3(x, y, computeZ(x - dx1, y - dy1, c1, k1));

    lens.vertices.push(point);

    for (var irad = 1; irad <= nrad; irad ++)
    {
        for (var itheta = 0; itheta < ntheta; itheta ++)
        {
            r = irad/nrad * surf1.surfaceRadius;
            theta = - itheta/ntheta * 2 * Math.PI;

            x = r * Math.cos(theta);
            y = r * Math.sin(theta);
            point = new THREE.Vector3(x, y, computeZ(x - dx1, y - dy1, c1, k1));

            lens.vertices.push(point);

        }
        if (irad ===1 )
        {
            for (var ipt = 0; ipt < ntheta; ipt ++)
            {
                lens.faces.push(new THREE.Face3(ipt + 1, (ipt + 1) % ntheta + 1, 0));
            }
        }
        else
        {
            for (var ipt = 0; ipt < ntheta; ipt ++)
            {
                var id1 = ipt + 1 + (irad-1) * ntheta;
                var id2 = (ipt + 1) % ntheta + 1 + (irad -1) * ntheta;
                var id3 = ipt + 1 + (irad -2) * ntheta;
                var id4 = (ipt + 1) % ntheta + 1 + (irad -2) * ntheta;

                lens.faces.push(new THREE.Face3(id1, id2, id3));
                lens.faces.push(new THREE.Face3(id3, id2, id4));
            }
        }
    }


    for (var irad = nrad; irad > 0; irad --)
    {
        for (var itheta = 0; itheta < ntheta; itheta ++)
        {
            r = irad/nrad * surf1.surfaceRadius;
            theta = - itheta/ntheta * 2 * Math.PI;

            x = r * Math.cos(theta);
            y = r * Math.sin(theta);
            point = new THREE.Vector3(x, y, surf1.surfaceThickness - computeZ(x - dx2, y - dy2, c2, k2));

            lens.vertices.push(point);

        }

        for (var ipt = 0; ipt < ntheta; ipt ++)
        {
            var id1 = ipt + 1 + (nrad * 2 - irad) * ntheta;
            var id2 = (ipt + 1) % ntheta + 1 + (nrad * 2 - irad) * ntheta;
            var id3 = ipt + 1 + (nrad * 2 - irad -1) * ntheta;
            var id4 = (ipt + 1) % ntheta + 1 + (nrad * 2 - irad -1) * ntheta;

            lens.faces.push(new THREE.Face3(id1, id2, id3));
            lens.faces.push(new THREE.Face3(id3, id2, id4));
        }


        if (irad === 1 )
        {
            x = 0;
            y = 0;

            point = new THREE.Vector3(x, y, surf1.surfaceThickness - computeZ(x - dx2, y - dy2, c2, k2));
            lens.vertices.push(point);

            for (var ipt = 0; ipt < ntheta; ipt ++)
            {
                lens.faces.push(new THREE.Face3((nrad * 2 - 1) * ntheta + ipt + 1, (nrad * 2) * ntheta + 1 , (nrad * 2 - 1)* ntheta + (ipt + 1) % ntheta + 1));
            }
        }
    }

    lens.computeVertexNormals();
    return lens
}