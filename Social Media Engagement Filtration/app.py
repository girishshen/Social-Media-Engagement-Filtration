from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__, static_folder='static')

# Load & preprocess data once
df = pd.read_csv('data/cleaned/Cleaned_Data.csv')

#df[['Views','Likes','Shares','Comments']] = df[['Views','Likes','Shares','Comments']].astype(int)
#df['Total_Engagement'] = df[['Likes','Shares','Comments']].sum(axis=1)
#df['Virality_Score']   = (2*df['Shares'] + df['Likes'] + df['Comments']) / df['Views']

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    # Get filters from form
    platform = request.form.get('platform', 'All')
    content_type = request.form.get('content_type', 'All')
    sort_by = request.form.get('sort_by', 'Total_Engagement')

    # Validate sort field
    if sort_by not in ['Views', 'Likes', 'Shares', 'Comments',
                       'Total_Engagement', 'Engagement_Rate', 'Virality_Score']:
        sort_by = 'Total_Engagement'

    # Filter and sort data
    data = df.copy()
    if platform != 'All':
        data = data[data['Platform'] == platform]

    if content_type != 'All':
        data = data[data['Content_Type'] == content_type]

    data = data.sort_values(by=sort_by, ascending=False)

    # Prepare options for dropdowns
    platforms = ['All'] + sorted(df['Platform'].unique())
    content_types = ['All'] + sorted(df['Content_Type'].unique())
    sort_options = ['Views', 'Likes', 'Shares', 'Comments',
                    'Total_Engagement', 'Engagement_Rate', 'Virality_Score']

    return render_template(
        'dashboard.html',
        tables=data.head(20).to_dict(orient='records'),
        platforms=platforms,
        content_types=content_types,
        sort_options=sort_options,
        platform_selected=platform,
        content_selected=content_type,
        sort_by=sort_by
    )

@app.route('/export')
def export_csv():
    # Reapply filters for export
    buf = io.StringIO()
    platform = request.args.get('platform', 'All')
    content_type = request.args.get('content_type', 'All')
    sort_by = request.args.get('sort_by', 'Total_Engagement')

    # Validate sort field
    if sort_by not in ['Views', 'Likes', 'Shares', 'Comments',
                       'Total_Engagement', 'Engagement_Rate', 'Virality_Score']:
        sort_by = 'Total_Engagement'

    # Filter and sort data
    data = df.copy()

    if platform != 'All':
        data = data[data['Platform'] == platform]

    if content_type != 'All':
        data = data[data['Content_Type'] == content_type]

    data = data.sort_values(by=sort_by, ascending=False)

    data.to_csv(buf, index=False)
    buf.seek(0)

    return send_file(
        io.BytesIO(buf.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='filtered_data.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)