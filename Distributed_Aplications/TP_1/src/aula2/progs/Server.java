package aula2.progs;
import aula2.interfaces.*;
import aula2.progs.PCmanager;


import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.rmi.server.RemoteStub;
import java.rmi.server.UnicastRemoteObject;


public class Server implements java.io.Serializable{
    public static void main(String[] args) {
        System.setProperty("java.rmi.server.hostname", "127.0.0.1");

        String name = "alves.LDA";
        PCmanager pc = null;

        try {
            pc = new PCmanager();
            //PCmanager gestor = pc.load_from("fc.dat");

            Registry registry = null;
            //LocateRegistry.createRegistry(1099);

            registry = LocateRegistry.getRegistry();

            //PCmanagerinterf stub = (PCmanagerinterf) UnicastRemoteObject.exportObject(pc,0);

            Remote stub = UnicastRemoteObject.exportObject(pc,0);

            GestorInt gestorInt = (GestorInt) stub;


            MedicoInt med = (MedicoInt) stub;

            UtenteInt u = (UtenteInt) stub;

            FuncionarioInt func = (FuncionarioInt) stub;

            registry.rebind(name, med);
            registry.rebind(name, gestorInt);
            registry.rebind(name, u);
            registry.rebind(name, func);

            System.out.println("Arranquei o Servidor");

        } catch (RemoteException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }
}
