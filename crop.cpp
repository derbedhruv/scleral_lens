#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
 
using namespace cv;
using namespace std;
Point corner;
Rect box;
Mat img, cropped;		   // this is used to read and write the images in matrix co-ordinates
int down=0,up=0;

void CallBackFunc(int event, int x, int y, int flags, void* userdata)
{
    if ( event == EVENT_LBUTTONDOWN )
    {
        down = 1;
        box.x = x;
	box.y = y;
    }
    
    if ( event == EVENT_LBUTTONUP )
    {
        up = 1;
        box.width = (abs(x-box.x));
	box.height = (abs(y - box.y));
        box.x=min(box.x, x);
        box.y=min(box.y, y);
        
    }
    
     if( up == 1 && down == 1)
    {
    	cropped = img(box).clone();		//copying the rectangular part of the image to a new image
	imwrite("images/Tiff images/cropped.tiff", cropped);
	imshow("Cropped Image",cropped); //showing the cropped image
        down=0;
        up=0;
    }

} 

int main()
{
	
	img = imread("images/Tiff images/report.tiff", CV_LOAD_IMAGE_ANYDEPTH | CV_LOAD_IMAGE_COLOR);	//reading in the image
	namedWindow("Image", CV_WINDOW_AUTOSIZE);
	imshow("Image",img);
	setMouseCallback("Image", CallBackFunc);	//this point will be used to get imput through mouse co-ordinated

	while(char(waitKey(1)!='q')) 
   	{
 
   	}
    
	return 0;
}
