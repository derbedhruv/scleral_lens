#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>

using namespace cv;
using namespace std;


float verifyCircle(Mat dt, Point2f center, float radius, vector<Point2f> & inlierSet)
{
 unsigned int counter = 0;
 unsigned int inlier = 0;
 float minInlierDist = 2.0f;
 float maxInlierDistMax = 100.0f;
 float maxInlierDist = radius/25.0f;
 if(maxInlierDist<minInlierDist) maxInlierDist = minInlierDist;
 if(maxInlierDist>maxInlierDistMax) maxInlierDist = maxInlierDistMax;

 // choose samples along the circle and count inlier percentage
 for(float t =0; t<2*3.14159265359f; t+= 0.05f)
 {
     counter++;
     float cX = radius*cos(t) + center.x;
     float cY = radius*sin(t) + center.y;

     if(cX < dt.cols)
     if(cX >= 0)
     if(cY < dt.rows)
     if(cY >= 0)
     if(dt.at<float>(cY,cX) < maxInlierDist)
     {
        inlier++;
        inlierSet.push_back(Point2f(cX,cY));
     }
 }

 return (float)inlier/float(counter);
}


 void getCircle(Point2f& p1,Point2f& p2,Point2f& p3, Point2f& center, float& radius)
{
  float x1 = p1.x;
  float x2 = p2.x;
  float x3 = p3.x;

  float y1 = p1.y;
  float y2 = p2.y;
  float y3 = p3.y;

  // PLEASE CHECK FOR TYPOS IN THE FORMULA :)
  center.x = (x1*x1+y1*y1)*(y2-y3) + (x2*x2+y2*y2)*(y3-y1) + (x3*x3+y3*y3)*(y1-y2);
  center.x /= ( 2*(x1*(y2-y3) - y1*(x2-x3) + x2*y3 - x3*y2) );

  center.y = (x1*x1 + y1*y1)*(x3-x2) + (x2*x2+y2*y2)*(x1-x3) + (x3*x3 + y3*y3)*(x2-x1);
  center.y /= ( 2*(x1*(y2-y3) - y1*(x2-x3) + x2*y3 - x3*y2) );

  radius = sqrt((center.x-x1)*(center.x-x1) + (center.y-y1)*(center.y-y1));
  
  
}



vector<Point2f> getPointPositions(Mat binaryImage)
{
 vector<Point2f> pointPositions;

 for(unsigned int y=0; y<binaryImage.rows; ++y)
 {
     
     for(unsigned int x=0; x<binaryImage.cols; ++x)
     {
         
         if(binaryImage.at<unsigned char>(y,x) > 0) pointPositions.push_back(Point2f(x,y));
     }
 }

 return pointPositions;
}


int main()
{
   
    Mat color = imread("images/Tiff images/img11.tiff");
    Mat gray;
    cvtColor(color, gray, CV_BGR2GRAY);

    // now map brightest pixel to 255 and smalles pixel val to 0. this is for easier finding of threshold
    double min, max;
    minMaxLoc(gray,&min,&max);
    float sub = min;
    float mult = 255.0f/(float)(max-sub);
    Mat normalized = gray - sub;
    normalized = mult * normalized;
    imshow("normalized" , normalized);
    //--------------------------------


    
    Mat mask;
  
    threshold(normalized, mask, 100, 255, CV_THRESH_BINARY);



    vector<Point2f> edgePositions;
    edgePositions = getPointPositions(mask);

   //this distance transform, I did not understand.
    Mat dt;
    distanceTransform(255-mask, dt,CV_DIST_L1, 3);

 
    unsigned int nIterations = 0;

    Point2f bestCircleCenter;
    float bestCircleRadius;
    float bestCirclePercentage = 0;
    float minRadius = 50; //can change for smaller radius
    //float minCirclePercentage = 0.2f;
    float minCirclePercentage = 0.05f;  // at least 5% of a circle must be present? maybe more...

    int maxNrOfIterations = edgePositions.size();   

    for(unsigned int its=0; its< maxNrOfIterations; ++its)
    {
        //RANSAC: randomly choose 3 point and create a circle:
        //TODO: choose randomly but more intelligent, 
        //so that it is more likely to choose three points of a circle. 
        //For example if there are many small circles, it is unlikely to randomly choose 3 points of the same circle.
        unsigned int idx1 = rand()%edgePositions.size();
        unsigned int idx2 = rand()%edgePositions.size();
        unsigned int idx3 = rand()%edgePositions.size();

        // we need 3 different samples:
        if(idx1 == idx2) continue;
        if(idx1 == idx3) continue;
        if(idx3 == idx2) continue;

        // create circle from 3 points:
        Point2f center; float radius;
        getCircle(edgePositions[idx1],edgePositions[idx2],edgePositions[idx3],center,radius);

        // inlier set unused at the moment but could be used to approximate a (more robust) circle from alle inlier
        vector<Point2f> inlierSet;

        //verify or falsify the circle by inlier counting:
        float cPerc = verifyCircle(dt,center,radius, inlierSet);

        // update best circle information if necessary
        if(cPerc >= bestCirclePercentage)
            if(radius >= minRadius)
        {
            bestCirclePercentage = cPerc;
            bestCircleRadius = radius;
            bestCircleCenter = center;
        }

    }

    // draw if good circle was found
    if(bestCirclePercentage >= minCirclePercentage)
        if(bestCircleRadius >= minRadius);
        circle(color, bestCircleCenter,bestCircleRadius, Scalar(255,255,0),1);
        cout<< "The radius for this part is "<<bestCircleRadius<<"\n";

        imshow("output",color);
        imshow("mask",mask);
        waitKey(0); //fr dispaly time.

        return 0;
    }
