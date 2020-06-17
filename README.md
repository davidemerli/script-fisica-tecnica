# Tabelle di Fisica Tecnica per Informatici

Buongiorno e benvenuti alle Tabelle di Fisica Tecnica per Informatici

## Installing
TODO

## Usage
La GUI e' autoesplicativa
Se i dati inseriti non sono corretti / fuori range nelle tabelle vengono generate delle eccezioni visualizzate su console e la query NON viene visualizzata

Se i dati inseriti sono corretti viene invece effettuata una query su una o piu' tabelle e vengono effettuate le interpolazioni (singole o doppie a seconda del caso) e restitutiti i risultati sotto forma di tabella

La tabella conterra' in rosso la riga con i valori corretti. Se i valori inseriti non hanno un'entry precisa nella tabella allora la riga in rosso avra' i valori gia' interpolati e corretti. Vengono inoltre fornite tutte le righe da cui sono state prese le informazioni per l'interpolazione.

TODO: Aggiungere la possibilita' di mostrare il calcolo quando viene clickato un valore interpolato

### Backend queries

``` python
    fields_ids = ["P_sat_bar", "T_sat", "v_l", "dv", "v_v", "h_l", "dh", "h_v", "s_l", "ds", "s_v"]
    water_sat_p = read_form("Tabelle_Acqua_Fix.txt", fields_ids, start=5, end=84)
    water_sat_p.print_response(water_sat_p.query_table_1d(("P_sat_bar", 146.0)))
    parser = argparse.ArgumentParser(description="Read data from Fisica Tecnica per Informatici tables")
    parser.add_argument("sost")
    

    print(TABLES['table_name']['object']._groups)
    # ESEMPIO Query di vapore saturo (Necessita di due parametri indipedenti)
    Print(TABLES['table_name']['object'].query_table_2d(("T", 320), ("P_bar", 5.5)))
    # ESEMPIO Query con quality
    # 1 - Fai una normale query nella tabella di saturazione
    resp1 = TABLES['table_name']['object'].query_table_1d(("P_sat_bar", 0.95))
    print(resp1)
    # 2 - Usando quella riga fai una query fornendo una grandezza tra "h", "l", "s", "u", "x"
    print(TABLES['table_name']['object'].query_table_1d_qlt(resp1.row, ('x', 0.5)))
```

TODO

## Copyright

Copyright (c) 2020 Davide Merli & Dario Passarello, Studenti del Corso di Fisica Tecnica per Informatici 
