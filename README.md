# Scleral Contact Lens Fitting
##Estimation of radius of curvature of Sclera through Anterior Segment OCT Images

### Authors - Navya Sri Nizamkari, Darpan Sanghavi, Dhruv Joshi

This project is all about estimation of scleral topography in four directions - nasal, temporal, superior and inferior, using AS-OCT Images taken at the LV Prasad Eye Institute, Hyderabad. The software is being developed at the Srujana Center for Innovation, LVPEI. 

Our intention is to make a software frontend which would enable clinicians to estimate these values from images quickly. These will then be correlated to fitting parameters in the contant lens.

## To compile and run
Run 
```
`g++ crop.cpp -o crop `pkg-config opencv --cflags --libs`
```
