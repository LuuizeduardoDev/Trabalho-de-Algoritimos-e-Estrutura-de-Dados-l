
public class Ordenacao_Notas {

    public static void main(String[] args) {

        double[] notas = {5.4, 3.6, 8.2, 6.5, 7.2};

        
        // quantas vezes o loop vai ser execultado com base no index do vetor, seguindo a regra do último index valido.
        for (double i = 0.0; i < notas.length -1; i++) {
            
            // loop compara os elementos adjacentes 
            for (int j = 0; j < notas.length -1 - i; j++ ){
                // funcao para sobrescrever o valor anterior
                if (notas[j] > notas[j + 1]) {

                    double temp = notas[j];
                    notas[j] = notas[j + 1];
                    notas[j + 1] = temp;
                }
            }
        }

        for (double ordernacao : notas) {
            System.out.print(ordernacao + " ");
        }
    }

}