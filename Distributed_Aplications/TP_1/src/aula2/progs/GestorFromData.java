/*package aula2.progs;

import aula2.exceptions.UtenteNaoExisteException;
import aula2.processoclinico.Medico;
import aula2.processoclinico.Utente;

import java.io.IOException;
import java.rmi.RemoteException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.UUID;

public class GestorFromData {

    public static void main(String[] args) throws RemoteException {
        try {
            //PCmanager gestor = PCmanager.load_from("fc.dat");
            //gestor.AdicionaUtente("Joaquina Miranda","Rua José Antunes","123456789","12450298 ZYX", LocalDate.now(),"1234","917785493","912523242","joaquina@gmail.com");
            //gestor.AdicionaFunc("Joaquina Miranda","Rua José Antunes","123456789","12450298 ZYX", LocalDate.now(),1234);

            //System.out.println(gestor.LoginUtente("1234","123456789"));
            //System.out.println(gestor.LoginUtente("1233","123456789"));
            //System.out.println(gestor.LoginUtente("1234","123456781"));

            //System.out.println(gestor.LoginMedico("0975-351","PT578156593"));
            //System.out.println(gestor.LoginMedico("097-0351","PT578156593"));

            //System.out.println(gestor.LoginFunc(1,"PT675375100"));
            //System.out.println(gestor.LoginFunc(1,"PT67537500"));

            //System.out.println(gestor.getUtente("0460925160759"));
            //System.out.println(gestor.getAgenda());
            //Utente utente = new Utente("Joaquina Miranda","Rua José Antunes","123456789","12450298 ZYX", LocalDate.now(),"1234","917785493","912523242","joaquina@gmail.com");
            //System.out.println(gestor.marca_consulta(utente,LocalDate.of(2020,11,29), LocalTime.of(14,00),"Urologia"));

            //System.out.println(gestor.marca_consulta(utente,LocalDate.of(2020,11,29), LocalTime.of(14,00),"Urologia"));

            //System.out.println(gestor.marca_consulta(utente,LocalDate.of(2020,11,30), LocalTime.of(14,00),"Reumatologia"));
            //System.out.println(gestor.marca_consulta(utente,LocalDate.of(2020,11,29), LocalTime.of(14,35),"Urologia"));
            //System.out.println(gestor.marca_consulta(utente,LocalDate.of(2020,11,29), LocalTime.of(14,35),"Urologia"));
            //System.out.println(gestor.getAgenda());


            //gestor.verlistaUtentes();
            //System.out.println(gestor.getAgenda());
            //gestor.cancelar_consulta(utente.getNumutente(), LocalDate.of(2020,11,29),LocalTime.of(14,00),"Urologia");
            //UUID num = gestor.realizarConsulta("1234",LocalDate.of(2020,11,29),  LocalTime.of(14, 00), 60.00,160, 1.00, 200, 300, 250, 1, 12);
            //System.out.println(gestor.getConsultas());
            //gestor.adicionarObservacoes(num,"Ta bom de saude!");

            //gestor.adicionar_prescricoes(num, LocalDate.of(2020,11,29), "2 vezes", "Abacavir","Ziagen","Comprimido revestido por película","300 mg","Autorizado",false,"ViiV Healthcare UK Ltd.");
            //System.out.println(gestor.getConsultas());

            //gestor.adicionar_historico("es grande","1234");
            //gestor.ver_fichaMedica("1234");

            //gestor.ver_fichaMedica("0460925160759");


            //gestor.consultas_utente("1234");

           // gestor.marca_exame(num,1234,"olhos","braga",LocalDate.of(2020,12,29), LocalTime.of(14, 00), LocalTime.of(00, 20),50.50,true, new ArrayList<String>());



            //gestor.utentes_idade(1931);
            //System.out.println(gestor.getFuncionarios());
            //System.out.println(gestor.getFichasUtente());
            //System.out.println(gestor.getMedicamentos().size());

            //gestor.save_to("fc.dat");


        } catch (IOException e) {
            e.printStackTrace();
            PCmanager gestor = new PCmanager();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
            PCmanager gestor = new PCmanager();
        }
    }
}
*/