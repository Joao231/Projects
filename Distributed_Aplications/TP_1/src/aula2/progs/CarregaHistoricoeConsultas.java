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
import java.util.Map;

public class CarregaHistoricoeConsultas {
    public static void main(String[] args) throws RemoteException {
        try {
            Registry reg = LocateRegistry.getRegistry("Localhost",1099);
            MedicoInt medico = (MedicoInt) reg.lookup("alves.LDA");
            GestorInt g = (GestorInt) reg.lookup("alves.LDA");
            BufferedReader br = null;
            try {
                br = new BufferedReader(new FileReader("/Users/joaom/uminho/AD/TP_1/src/aula2/ficheiros/fichautentes.txt"));
                String line;
                Map<String, FichaMedica> fichasUtente = medico.getFichasUtente();
                while ((line = br.readLine()) != null) {
                    String []tokens = line.split(";");
                    for (int i = 0; i < tokens.length; i++) {
                        if (tokens[i].startsWith("\"")) {
                            tokens[i] = tokens[i].replace('"', ' ').strip();
                        }
                    }


                    //if (!fichasUtente.containsKey(tokens[0])) {
                        //throw new UtenteNaoExisteException();
                    //}
                    medico.adicionar_historico(tokens[1], tokens[0]);
                }
                br.close();
                medico.save_to("fc.dat");

                Map<String, Medico> medicos = g.getMedicos();
                Map<String, Medicamento> medicamentos = g.getMedicamentos();
                br = new BufferedReader( new FileReader("/Users/joaom/uminho/AD/TP_1/src/aula2/ficheiros/consultas.txt"));
                while( (line = br.readLine()) != null){
                    String []tokens = line.split(";");
                    for(int i=0 ; i < tokens.length; i++){
                        if (tokens[i].startsWith("\"")){
                            tokens[i] = tokens[i].replace('"',' ').strip();
                        }
                    }
                    String []data = tokens[2].split("-");



                    //if (! medicos.containsKey(tokens[0])){
                        //throw new MedicoNaoExisteException();
                    //}
                    Medico m = medicos.get(tokens[0]);



                    //if (! fichasUtente.containsKey(tokens[1])){
                        //throw  new UtenteNaoExisteException();
                    //}

                    Consulta co = g.adicionar_consulta(m, tokens[1], tokens[3]);


                    for(int i = 4; i < tokens.length; i++){
                        String token = tokens[i];
                        token = token.
                                replace('[',' ').
                                replace( ']',' ').
                                strip();
                        String[] rtokens = token.split(",");
                        for(int j=0 ; j < rtokens.length; j++){
                            rtokens[j] = rtokens[j].replace('\'',' ').strip();
                        }
                        data = rtokens[0].split("-");

                        //if(! medicamentos.containsKey(rtokens[1])){
                            //throw new MedicamentoNaoExisteException();
                        //}
                        Medicamento medc = medicamentos.get(rtokens[1]);
                        g.criar_prescricoes(co,tokens[1],LocalDate.of(
                                Integer.parseInt(data[0]),
                                Integer.parseInt(data[1]),
                                Integer.parseInt(data[2])),
                                medc, rtokens[2]);
                    }

                }
                g.save_to("fc.dat");
                System.out.println("Consultas e fichas utentes adicionadas!");
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } //catch (MedicoNaoExisteException e) {
                //e.printStackTrace();
             //catch (MedicamentoNaoExisteException e) {
                //e.printStackTrace();
            //} //catch (UtenteNaoExisteException e) {
                //e.printStackTrace();

        } catch (RemoteException remoteException) {
            remoteException.printStackTrace();
        } catch (NotBoundException notBoundException) {
            notBoundException.printStackTrace();
        }
    }
}
