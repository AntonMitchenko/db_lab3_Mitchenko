DO $$
 DECLARE
     name_of_wonder wonder_of_world.name_of_wonder%TYPE;
     type_of_wonder wonder_of_world.type_of_wonder%TYPE;
	 build_in_year  wonder_of_world.build_in_year%TYPE;
	
 BEGIN
     name_of_wonder := 'name';
	 type_of_wonder := 'type';
     build_in_year := 'date';
     FOR counter IN 0...10
         LOOP
            INSERT INTO wonder_of_world (name_of_wonder, type_of_wonder, build_in_year)
             VALUES (name_of_wonder || counter, type_of_wonder || counter,build_in_year || counter);
         END LOOP;
 END;
 $$
 