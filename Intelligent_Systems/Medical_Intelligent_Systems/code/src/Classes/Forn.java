package Classes;

import java.util.HashMap;
import jade.core.AID;

public class Forn implements java.io.Serializable{
	private AID agent;
	
	private HashMap<String, Integer> med_preco = new HashMap<>();
	
	public Forn(AID agent) {
		
		this.agent = agent;
	}
	
	public AID getAgent() {
		return agent;
	}
	
	public HashMap<String, Integer> getMed_preco() {
		return med_preco;
	}

	public void setSMed_preco(HashMap<String, Integer> med_preco) {
		this.med_preco = med_preco;
	}
	
	public Integer buscar_preco_med(String medicamento){
		   return med_preco.get(medicamento);
	}	
}

