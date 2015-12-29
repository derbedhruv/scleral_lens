/****************************************
  SCLERAL TOPOGRAPHY ESTIMATION

  AUTHORS: Navya sri Nizamkari, Darpan Sanghavi, Dhruv Joshi

****************************************/

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
 
using namespace cv;
using namespace std;
Point corner;
Rect box;
Mat img, cropped, cropped2;		   // this is used to read and write the images in matrix co-ordinates
int down=0,up=0;

void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
    if ( event == EVENT_LBUTTONDOWN )
    {
        down = 1;
        box.x = x;
	    box.y = y;
        std::cout<<" button down: "<<x<<" , "<<y<<std::endl;
    }
    
    if ( event == EVENT_LBUTTONUP && box.x != x && box.y != y )
    {
        up = 1;
        box.width = (abs(x-box.x));
	box.height = (abs(y - box.y));
        box.x=min(box.x, x);
        box.y=min(box.y, y);
        std::cout<<" button up: "<<x<<" , "<<y<<std::endl;
    }
    
     if( up == 1 && down == 1)
    {
    	cropped2 = cropped(box).clone();		//copying the rectangular part of the image to a new image
	    imwrite("images/Tiff/cropped2_borders.tiff", cropped2);
	    //imshow("Cropped Image",cropped); //showing the cropped image
        down=0;
        up=0;
        std::cout<<"Done."<<std::endl;
        exit(0);
    }

} 

int main() {
	
	// reading in and displaying the image
	img = imread("images/Tiff/report_borders.tiff", CV_LOAD_IMAGE_ANYDEPTH | CV_LOAD_IMAGE_COLOR);

	//namedWindow("Image", CV_WINDOW_AUTOSIZE);
    //namedWindow("Image", CV_WINDOW_NORMAL);

	//imshow("Image", img);

    box.x = 57; 
    box.y = 407;
    box.width = 1100;
    box.height = 500;
    cropped = img(box).clone();

    imwrite("images/Tiff/cropped_borders.tiff", cropped);
    namedWindow("Scan",CV_WINDOW_NORMAL);
    imshow("Scan", cropped);

	setMouseCallback("Scan", CallBackFunc);	//this point will be used to get imput through mouse co-ordinated

	while(char(waitKey(1)!='q')) {
 	  // do stuff and exit by pressing q
   	}
    
	return 0;
}
