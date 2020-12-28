import { Reference } from '@/library/context';
import { Collection } from '@/library/types';
import React, { ChangeEvent, useContext } from 'react';
import InputField, { InputFieldComponent } from '@/components/generic/input-field';

interface CountryInputComponent extends InputFieldComponent {
    onValueChange: (value: string | null) => void;
}

const CountryInput: React.FC<CountryInputComponent> = ({ defaultValue, onValueChange, ...props }) => {
    const Ref = useContext(Reference);
    const onClick = (e: React.MouseEvent<HTMLInputElement>) => e.currentTarget.select();
    const [countries, setCountries] = useState<Collection>(Ref?.countries || {});
    const find = (key?: string): string | undefined => {
        return Object.keys(countries).find(c =>
            c.toLowerCase() === key?.toLowerCase() ||
            countries[c].toLowerCase() === key?.toLowerCase()
        );
    };
    const onChange = (e: ChangeEvent<any>) => {
        e.preventDefault();
        let value = find(e.target.value);
        onValueChange(value || e.target.value);
    };
    useEffect(() => {
        if (Ref !== undefined) {
            setCountries(Ref.countries);
        }
    }, [countries]);

    return (
        <InputField onChange={onChange} onClick={onClick} defaultValue={Ref?.countries[defaultValue as string]} list="countries" {...props}>
            <datalist id="countries">
                {Object
                    .entries(Ref?.countries as Collection || {})
                    .map(([code, name]) => <option key={code} value={name} />)
                }
            </datalist>
        </InputField>
    )
};

export default CountryInput;