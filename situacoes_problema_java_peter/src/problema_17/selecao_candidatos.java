package problema_17;


public class selecao_candidatos {
    public static void main(String[] args){

        int[] notas = {7, 14, 3, 19, 11, 8, 20, 5, 12, 1, 16, 9, 18, 4, 15};
        String[] candidatos = {"Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena", "Igor", "Juliana", "Lucas", "Mariana", "Nicolas", "Patrícia", "Rafael"};
        

        //loop controla qual posição está sendo prenchida, com o menor valor restante.
        for ( int i = 0; i < notas.length - 1; i++) {

            
            int minIndex = i;
            
            // loop busca menor elemento na parte restante ainda não ordenada.
            for (int j = i + 1; j < notas.length; j++) {
                
                if (notas[j] < notas[minIndex]) {
                    minIndex = j;

                }
            }
             
            //função para trocar itens: nota  no array
            int temp = notas[i];
            notas[i] = notas[minIndex];
            notas[minIndex] = temp;

            //função para trocar itens: candidatos no array
            String tempCandidatos = candidatos[i];
            candidatos[i] = candidatos[minIndex];
            candidatos[minIndex] = tempCandidatos;

            
        }
        
        System.out.println("Rank\tNomes\tNotas");
        System.out.println("----------------------");
        
        
        
        for (int i = notas.length -1; i >= 0; i--) {

            int rank = notas.length - i;
            System.out.printf("%-6d %-12s %d%n", rank, candidatos[i], notas[i]);

             
        }
    }
    
}
