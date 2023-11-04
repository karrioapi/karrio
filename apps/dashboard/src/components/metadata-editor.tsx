import TextAreaField from '@/components/generic/textarea-field';
import InputField from '@/components/generic/input-field';
import { MetadataObjectTypeEnum } from 'karrio/graphql';
import { Loading } from '@/components/loader';
import React from 'react';
import MetadataStateProvider, { MetadataStateContext } from '@/context/metadata';

interface MetadataEditorProps {
  id?: string;
  metadata?: {};
  object_type: MetadataObjectTypeEnum;
  onChange?: (metadata: any) => void;
}
interface MetadataEditorInterface {
  editMetadata: () => void;
  isEditing: boolean
}

export const MetadataEditorContext = React.createContext<MetadataEditorInterface>({} as MetadataEditorInterface);


const MetadataEditor: React.FC<MetadataEditorProps> = ({ id, metadata, object_type, children, onChange }) => {
  const { loading } = React.useContext(Loading);
  const [isEditing, setIsEditing] = React.useState(false);

  const editMetadata = (context: any) => () => {
    if (Object.keys(context.state).length == 0) context.addItem();
    setIsEditing(true);
  };

  return (
    <>
      <MetadataStateProvider id={id} object_type={object_type} value={metadata}>
        <MetadataStateContext.Consumer>{(context) => (<>
          <MetadataEditorContext.Provider value={{ editMetadata: editMetadata(context), isEditing }}>

            {children}

            <div style={{ overflow: 'auto', maxHeight: '12em' }}>
              {Object.entries(context.state).map(
                ([uid, { key, value }], index) => <React.Fragment key={index + "-metadata"}>
                  <div className="is-flex columns my-1 mx-0" key={uid}>
                    <div className="column is-3 p-1">
                      {!isEditing && <span className="has-text-weight-semibold has-text-grey is-size-7 p-2">{key}</span>}
                      {isEditing && <InputField
                        placeholder="Key"
                        defaultValue={key}
                        onChange={(e: React.ChangeEvent<any>) => context.updateItem(uid, { key: e.target.value, value })}
                        className="is-small is-fullwidth"
                        required />}
                    </div>
                    <div className="column p-1">
                      {!isEditing && <span className="is-size-7">{value}</span>}
                      {isEditing &&
                        <TextAreaField
                          placeholder="Value"
                          defaultValue={value}
                          onChange={(e: React.ChangeEvent<any>) => context.updateItem(uid, { key, value: e.target.value })}
                          className="is-small is-fullwidth py-1"
                          style={{ minHeight: "30px" }}
                          rows={1}
                          required />}
                    </div>
                    {isEditing && <div className="p-1">
                      <button className="button is-white is-small" onClick={() => context.removeItem(uid)}>
                        <span className="icon is-small">
                          <i className="fas fa-trash"></i>
                        </span>
                      </button>
                    </div>}
                  </div>
                  {context.error?.key === key && <p className="has-text-danger px-2 is-size-7">
                    {context.error?.message}
                  </p>}
                </React.Fragment>
              )}
            </div>

            {!isEditing && Object.keys(context.state || {}).length == 0 && <div className="p-2 is-size-7">No metadata</div>}

            {isEditing && <>
              <hr className="mt-1 mb-2" style={{ height: '1px' }} />
              <div className="is-flex is-justify-content-space-between">
                <button
                  type="button"
                  className="button is-white is-small has-text-primary"
                  onClick={() => context.addItem()}
                >
                  <span className="icon is-small">
                    <i className="fas fa-plus"></i>
                  </span>
                  <span>Add another item</span>
                </button>

                <div className="field is-grouped">
                  <p className="control">
                    <button type="button" className="button is-small is-default"
                      onClick={() => { context.reset(); setIsEditing(false); }}>Cancel</button>
                  </p>
                  <p className="control">
                    <button
                      type="button"
                      className={`button is-small is-primary ${loading ? 'is-loading' : ''}`}
                      disabled={loading}
                      onClick={() => context.saveMetadata({
                        onChange: (metadata) => {
                          onChange && onChange(metadata);
                          setIsEditing(false);
                        }
                      })}
                    >Save</button>
                  </p>
                </div>
              </div>
            </>}

          </MetadataEditorContext.Provider>
        </>)}</MetadataStateContext.Consumer>
      </MetadataStateProvider>
    </>
  );
};

export default MetadataEditor;
