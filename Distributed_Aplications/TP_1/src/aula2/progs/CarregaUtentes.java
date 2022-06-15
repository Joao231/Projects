package aula2.progs;
import aula2.interfaces.*;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.time.LocalDate;

public class CarregaUtentes {
    public static void main(String[] args) throws RemoteException {
        try {
            Registry reg = LocateRegistry.getRegistry("Localhost",1099);
            FuncionarioInt f = (FuncionarioInt) reg.lookup("alves.LDA");
            try {
                BufferedReader br = null;
                br = new BufferedReader(new FileReader("/Users/joaom/uminho/AD/TP_1/src/aula2/ficheiros/utentes.txt"));
                String line;
                while ((line = br.readLine()) != null) {
                    String [] tokens = line.split(";");
                    for (int i = 0; i < tokens.length; i++) {
                        if (tokens[i].startsWith("\"")) {
                            tokens[i] = tokens[i].replace('"', ' ').strip();
                        }
                    }
                    String[] dn = tokens[4].split("-");
                    f.AdicionaUtente(tokens[0], tokens[1], tokens[2],
                            tokens[3], LocalDate.of(
                                    Integer.parseInt(dn[0]),
                                    Integer.parseInt(dn[1]),
                                    Integer.parseInt(dn[2])
                            ),
                            tokens[5], tokens[6], tokens[7], tokens[8]);
                }
            f.save_to("fc.dat");
            System.out.println("Utentes adicionados!");

            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }


        } catch (
                RemoteException remoteException) {
            remoteException.printStackTrace();
        } catch (NotBoundException notBoundException) {
            notBoundException.printStackTrace();
        }
    }

}
