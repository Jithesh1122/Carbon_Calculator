public class Practice3 {
    public static void main(String[] args) {
        float [] marks={44.3f,86.5f,99.8f,100.0f};
        for(int i=0;i<marks.length/2;i++){
           float s=marks[i];
           marks[i]=marks[marks.length-1-i];
           marks[marks.length-1-i]=s;
        }
        for (float f : marks) {
            System.out.print(f+" ");
        }

    }
}
