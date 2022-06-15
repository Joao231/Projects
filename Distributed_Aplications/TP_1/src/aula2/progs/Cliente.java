package aula2.progs;
import aula2.interfaces.*;
import aula2.exceptions.MedicamentoNaoExisteException;
import aula2.exceptions.MedicoNaoExisteException;
import aula2.exceptions.UtenteNaoExisteException;
import aula2.processoclinico.*;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Map;
import java.util.UUID;


public class Cliente {
    public static void main(String[] args) {
        try {

            Registry reg = LocateRegistry.getRegistry("Localhost",1099);
            GestorInt g = (GestorInt) reg.lookup("alves.LDA");
            FuncionarioInt f = (FuncionarioInt) reg.lookup("alves.LDA");
            UtenteInt u = (UtenteInt) reg.lookup("alves.LDA");
            MedicoInt medico = (MedicoInt) reg.lookup("alves.LDA");
            g.verlistaMedicos();
            //System.out.println(g.getMedicamentos());
            //System.out.println(g.getMedicos());
            //g.AdicionaMed("jose matos","Rua da trindade","PT223450055","888-60-0336",LocalDate.of(1967,04,14),"6757-768","Urologia");
            //System.out.println(medico.getFichasUtente().size());
            //f.AdicionaUtente("Joaquina Alves","Rua da Luz","123456789","88888888 ZYX", LocalDate.of(1931,10,29),"1234","939255568","929578854","joaquinaalves@gmail.com");
            //System.out.println(medico.getFichasUtente().size());
            //System.out.println(u.LoginUtente("1234","123456789"));
            //System.out.println(g.getFuncionarios());
            //System.out.println(medico.LoginMedico("0975-351","PT578156593"));
            //System.out.println(f.LoginFunc(1,"PT675375100"));
            //System.out.println(u.marca_consulta("1234",LocalDate.of(2020,11,29), LocalTime.of(14,00),"Urologia"));
            //System.out.println(u.marca_consulta("1234",LocalDate.of(2020,11,30), LocalTime.of(14,00),"Reumatologia"));
            //System.out.println(u.marca_consulta("1234",LocalDate.of(2020,11,29), LocalTime.of(14,00),"Urologia"));
            //System.out.println(u.marca_consulta("1234",LocalDate.of(2020,11,29), LocalTime.of(14,35),"Urologia"));
            //System.out.println(g.getAgenda());
            //u.cancelar_consulta("1234", LocalDate.of(2020,11,29),LocalTime.of(14,00),"Urologia");
            //UUID num = medico.realizarConsulta("1234",LocalDate.of(2020,11,29),  LocalTime.of(14, 00), 60.00,160, 1.00, 200, 300, 250, 1, 12);
            //System.out.println(g.getConsultas());
            //medico.adicionarObservacoes(num,"Ta bom de saude!");
            //System.out.println(g.getConsultas());
            //medico.adicionar_prescricoes(num, LocalDate.of(2020,11,29), "2 vezes", "Abacavir","Ziagen","Comprimido revestido por película","300 mg","Autorizado",false,"ViiV Healthcare UK Ltd.");
            //System.out.println(g.getConsultas());

           // medico.adicionar_historico("es grande","1234");


            //medico.consultas_utente("1234");

            //medico.marca_exame(num,1234,"olhos","braga",LocalDate.of(2020,12,29), LocalTime.of(14, 00), LocalTime.of(00, 20),50.50,true, new ArrayList<String>());


            //System.out.println(g.getConsultas());
            //medico.ver_fichaMedica("1234");
            //g.utentes_idade(1931);
            //System.out.println(medico.getFichasUtente());
            //System.out.println(g.getFuncionarios());

        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}










