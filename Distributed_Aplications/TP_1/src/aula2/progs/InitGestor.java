/*package aula2.progs;

import aula2.exceptions.MedicamentoNaoExisteException;
import aula2.exceptions.MedicoNaoExisteException;
import aula2.exceptions.UtenteNaoExisteException;
import aula2.exceptions.UtenteJaExisteException;

import java.io.IOException;
import java.rmi.RemoteException;

public class InitGestor {
    public static void main(String[] args) throws RemoteException {
        PCmanager gestor = new PCmanager();
        gestor.load_meds("/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/lista_infomed_2020.csv");
        gestor.load_funcionarios("/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/funcionarios.txt");
        gestor.load_medicos("/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/medicos.txt");
        gestor.load_utentes("/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/utentes.txt");
        try {
            gestor.load_histUtentes("/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/fichautentes.txt",
                    "/Users/paulo/Ambiente de Trabalho/MESTRADO/AD/TP_1/src/aula2/ficheiros/consultas.txt");
        } catch (UtenteNaoExisteException e) {
            e.printStackTrace();
        } catch (MedicoNaoExisteException e) {
            e.printStackTrace();
        } catch (MedicamentoNaoExisteException e) {
            e.printStackTrace();
        }
        System.out.println(gestor.getFichasUtente().size());
        System.out.println(gestor.getFuncionarios().size());

        try {
            gestor.save_to("fc.dat");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
*/