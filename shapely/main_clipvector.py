import  VectorClipByVector
import  sys
import os
if __name__=="__main__":
    algomethod=sys.argv[1]
    input_Basepath=sys.argv[2]
    input_Clippath=sys.argv[3]
    output_path=sys.argv[4]
if algomethod=="Clip":
   VectorClipByVector.VectorClipByVectorNew(input_Basepath,input_Clippath,output_path)
elif algomethod=="Intersect":
   VectorClipByVector.VectorInterSect(input_Basepath,input_Clippath,output_path)

