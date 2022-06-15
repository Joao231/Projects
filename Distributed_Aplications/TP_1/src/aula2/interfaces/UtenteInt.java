package aula2.interfaces;
import java.io.IOException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.UUID;


public interface UtenteInt extends Remote{

    public String LoginUtente(String numutente, String nif ) throws RemoteException;

    public String marca_consulta(String numutente, LocalDate data, LocalTime hora, String especialidade) throws RemoteException, IOException;

    public void consultas_utente(String numutente) throws RemoteException;

    public void exames_utente(String numutente) throws RemoteException;

    public int cancelar_consulta(String numutente, LocalDate data, LocalTime hora, String especialidade) throws RemoteException;

}
