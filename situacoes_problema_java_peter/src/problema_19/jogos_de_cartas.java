package problema_19;


public class jogos_de_cartas {
   static void insertionSort(int[] carta) {
    int n = carta.length;
    
    // Loop seleciona o próximo elemento a ser inserido na parte ordenada do array.
    for (int i = 1; i < n; ++i) {
        int key = carta[i];
        int j = i - 1;
            // Condição fundamental do Insertion Sort
            while (j >= 0 && carta[j] > key) {
                // copia o elemento maior para a posição imediatamente à sua direita
                carta[j + 1] = carta[j];
                j = j - 1;
            }
            carta[j + 1] = key;
            printArray(carta);
        }
   
    }
    static void printArray(int[] carta) {
        for (int x : carta) {
            System.out.print(x + " ");
        }
        System.out.println();
    }
    
    public static void main(String[] args) {
        int[] carta = {7, 3, 8, 8, 1, 9, 4, 10, 2, 5};
        System.out.print("Cartas antes de organizar: ");
        printArray(carta);

        insertionSort(carta);
        
    }

}  
