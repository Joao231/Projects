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

public class CarregaMedicamentos {
    public static void main(String[] args) throws RemoteException {
        try {

            Registry reg = LocateRegistry.getRegistry("Localhost", 1099);
            GestorInt g = (GestorInt) reg.lookup("alves.LDA");
            BufferedReader br = null;

            try {
                br = new BufferedReader(new FileReader("/Users/joaom/uminho/AD/TP_1/src/aula2/ficheiros/lista_infomed_2020.csv"));
                String line;
                while ((line = br.readLine()) != null) {
                    String[] tokens = line.split(";");
                    g.AdicionaMec(tokens[0],tokens[1], tokens[2],
                            tokens[3], tokens[4],
                            tokens[5], Boolean.getBoolean(tokens[6]),
                            tokens[7]
                    );
                }
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            g.save_to("fc.dat");
            System.out.println("Medicamentos adicionados!");
        } catch (RemoteException remoteException) {
            remoteException.printStackTrace();
        } catch (NotBoundException notBoundException) {
            notBoundException.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
