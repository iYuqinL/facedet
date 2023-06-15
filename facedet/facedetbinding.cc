/**
 * File: facedetbinding.cc
 * Created Date: Wednesday, June 14th 2023, 10:47:54 pm
 * Author: iYuqinL
 * -----
 * Last Modified: Thu Jun 15 2023
 * Modified By: iYuqinL
 * -----
 * Copyright © 2023 iYuqinL Holding Limited
 * 
 * All shall be well and all shall be well and all manner of things shall be well.
 * Nope...we're doomed!
 * -----
 * HISTORY:
 * Date      	By	Comments
 * ----------	---	----------------------------------------------------------
**/
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <vector>

#include "facedetcnn.h"


//define the buffer size. Do not change the size!
//0x9000 = 1024 * (16 * 2 + 4), detect 1024 face at most
#define DETECT_BUFFER_SIZE 0x9000

using namespace std;
namespace py = pybind11;


vector<vector<int>> detect_face(py::array_t<uint8_t>& imarr)
{
    int rows = imarr.shape(0);   // image height
    int cols = imarr.shape(1);   // image width
    int channels = imarr.shape(2);
    // cout << "rows: " << rows << " cols: " << cols
    //      << " channels: " << channels << std::endl;
    assert(channels == 3);
    int * pResults = NULL;
    //pBuffer is used in the detection functions.
    //If you call functions in multiple threads, please create one buffer for each thread!
    unsigned char * pBuffer = (unsigned char *)malloc(DETECT_BUFFER_SIZE);
    if(!pBuffer)
    {
        cout << "Can not alloc buffer.\n";
        return {};
    }

    cout << "imarr strides(0): " << imarr.strides(0) << endl;

    pResults = facedetect_cnn(
        pBuffer, (unsigned char*)(imarr.data()),
        cols, rows, (int)(imarr.strides(0)));

    vector<vector<int>> res;
    for(int i = 0; i < (pResults ? *pResults : 0); i++)
	{
        short * p = ((short*)(pResults + 1)) + 16*i;
		int confidence = p[0];
		int x = p[1];
		int y = p[2];
		int w = p[3];
		int h = p[4];

        vector<int> one_face = {
            confidence, x, y, w, h,
            p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14]};

        res.emplace_back(one_face);
    }
    return res;
}


PYBIND11_MODULE(pyfacedet, m){
    m.def("detect_face", &detect_face, "");
}