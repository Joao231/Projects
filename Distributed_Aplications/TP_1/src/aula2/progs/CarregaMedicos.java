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

public class CarregaMedicos {
    public static void main(String[] args) throws RemoteException {


        try {

            Registry reg = LocateRegistry.getRegistry("Localhost",1099);
            GestorInt g = (GestorInt) reg.lookup("alves.LDA");
            BufferedReader br = null;
            try {
                br = new BufferedReader(new FileReader("/Users/joaom/uminho/AD/TP_1/src/aula2/ficheiros/medicos.txt"));
                String line;
                while ((line = br.readLine()) != null) {
                    String []tokens = line.split(";");
                    for (int i = 0; i < tokens.length; i++) {
                        if (tokens[i].startsWith("\"")) {
                            tokens[i] = tokens[i].replace('"', ' ').strip();
                        }
                    }

                    String[] dn = tokens[4].split("-");
                    g.AdicionaMed(tokens[0], tokens[1], tokens[2],
                            tokens[3], LocalDate.of(Integer.valueOf(dn[0]),
                                    Integer.valueOf(dn[1]),
                                    Integer.valueOf(dn[2])),
                            tokens[5], tokens[6]);
                }
            g.save_to("fc.dat");
            System.out.println("Medicos adicionados!");

            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (RemoteException remoteException) {
            remoteException.printStackTrace();
        } catch (NotBoundException notBoundException) {
            notBoundException.printStackTrace();
        }


    }

}
