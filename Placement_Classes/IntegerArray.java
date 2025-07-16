public class IntegerArray {
    public static void main(String[] args) {
        int[] arr = {10,4,0,8,5,0,3,0,7};
        int k=0;
        for(int i=0;i<arr.length;i++){
            if(arr[i]!=0){
                arr[k++]=arr[i];
            }
        }
        for(int i=k;i<arr.length;i++){
            arr[i]=0;
        }
        System.out.println("Array after moving zeros to end:");
        for(int i=0;i<arr.length;i++){
            System.out.print(arr[i]+" ");
        }
    }
}
