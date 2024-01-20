create event if not exists `tickets_by_faculties_scopes_stats` on schedule
        every 1 hour
    on completion not preserve
    enable
    comment 'Calculate statistics for faculties and scopes'
    do
        create or replace view tickets_by_faculties_scopes as (
            select
                f.faculty_id,
                f.name,
                count(q_r.scope) as "Reports",
                count(q_q.scope) as "Q/A",
                count(q_s.scope) as "Suggestion"
            from faculties f
            left join tickets t on (
                t.faculty_id = f.faculty_id
                and t.created > date(now() - interval 1 month)
                )
            left join queues q_r on (
                        t.queue_id = q_r.queue_id
                    and q_r.scope = 'Reports'
                )
            left join queues q_q on (
                        t.queue_id = q_q.queue_id
                    and q_q.scope = 'Q/A'
                )
            left join queues q_s on (
                        t.queue_id = q_s.queue_id
                    and q_s.scope = 'Suggestion'
                )
            group by f.faculty_id
        );

create event if not exists `tickets_by_statuses_stats` on schedule
        every 1 hour
    on completion not preserve
    enable
    comment 'Calculate statistics for tickets by statuses'
    do
        create or replace view tickets_by_statuses as (
            select
                statuses.*, count(ticket_id) tickets_count
            from statuses
                left join (
                    select ticket_id, status_id
                    from tickets
                    where created > date(now() - interval 1 month)
                    ) tickets_for_last_month
                using (status_id)
            group by statuses.status_id
        );

create event if not exists `tickets_by_scopes_stats` on schedule
        every 1 hour
    on completion not preserve
    enable
    comment 'Calculate statistics for tickets by statuses'
    do
        create or replace view tickets_by_scopes as (
            select
                distinct scope, count(ticket_id) tickets_count
            from queues q
            left join tickets t on (
                    q.queue_id = t.queue_id
                    and t.created > date(now() - interval 1 month)
                    )
            group by scope
        );
