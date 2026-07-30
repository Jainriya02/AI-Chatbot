import { MessageType } from "../types";

interface Props {
  message: MessageType;
}

export default function Message({ message }: Props) {
  if (message.role === "user") {
    return (
      <div className="text-right">

        <div className="inline-block bg-blue-600 text-white p-3 rounded-lg">

          {message.content}

        </div>

      </div>
    );
  }

  return (
    <div>

      <div className="bg-gray-100 p-4 rounded-lg">

        <p>{message.content}</p>

        {message.response && (
          <>
            <hr className="my-4" />

            <p>
              <strong>Tool Used:</strong>{" "}
              {message.response.tool}
            </p>

            {message.response.sql && (
              <>
                <h3 className="font-semibold mt-4">
                  Generated SQL
                </h3>

                <pre className="bg-white border rounded p-3 overflow-auto">
{message.response.sql}
                </pre>
              </>
            )}

            {message.response.citations &&
              message.response.citations.length > 0 && (
                <>
                  <h3 className="font-semibold mt-4">
                    Citations
                  </h3>

                  <ul className="list-disc ml-6">

                    {message.response.citations.map(
                      (citation, index) => (
                        <li key={index}>
                          {citation.file} (Page {citation.page})
                        </li>
                      )
                    )}

                  </ul>
                </>
              )}

          </>
        )}

      </div>

    </div>
  );
}